from PyQt4.QtCore import (Qt, QCoreApplication, QSettings, QThread,
    QTranslator, qVersion)
from PyQt4.QtGui import (QAction, QDialog, QIcon, QLabel, QPixmap,
    QProgressBar, QPushButton)
from qgis.core import (QgsContrastEnhancement, QgsMapLayerRegistry,
    QgsMessageLog, QgsRasterLayer)
from qgis.gui import QgsMessageBar

from natural_earth_raster_dialog import NaturalEarthRasterDialog
from natural_earth_raster_worker import NaturalEarthRasterWorker

import csv
import os.path
import resources_rc


class NaturalEarthRaster:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        # save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.themes = {'high': [], 'medium': [], 'low': []}

        csv_file = os.path.join(self.plugin_dir, 'data', 'natural_earth.csv')
        with open(csv_file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.themes[row[0]].append({'id': row[1], 'name': row[2],
                    'preview': row[3], 'url': row[4]})

        # declare instance attributes
        self.action = None
        self.menu = self.tr('&Natural Earth')

    def initGui(self):
        """Create the menu entries inside the QGIS GUI."""

        # create action to display the settings dialog
        self.action = QAction(
            QIcon(':/plugins/natural_earth_raster/assets/icon.png'),
            self.tr('Add theme...'),
            self.iface.mainWindow())

        # connect the actions to their respective methods
        self.action.triggered.connect(self.run)

        # add toolbar button and menu items
        self.iface.addPluginToRasterMenu(self.menu, self.action)

    def unload(self):
        """Removes the plugin menu item from the QGIS GUI."""

        self.iface.removePluginRasterMenu('&Natural Earth', self.action)

    def run(self):
        """Makes a few sanity checks and prepares the worker thread."""

        # create the dialog (after translation) and keep reference
        self.dialog = NaturalEarthRasterDialog()

        # connect some odds and ends
        self.dialog.scaleCombo.currentIndexChanged.connect(self.update_theme)
        self.dialog.themeCombo.currentIndexChanged.connect(self.update_preview)

        # make sure we have themes to choose from
        self.update_theme(0)

        # show the dialog
        self.dialog.show()
        result = self.dialog.exec_()
        if result == QDialog.Rejected:
            return False

        # get the indices of the selected combobox items
        scale = self.get_scale()
        theme = self.dialog.themeCombo.currentIndex()

        # build the path to the local copy of the theme
        id = self.themes[scale][theme]['id']
        theme_path = os.path.join(self.plugin_dir, 'data', id, id + '.tif')

        if os.path.isfile(theme_path):
            # we have a local copy of the theme, just add it to the workspace
            self.add_raster_layer(theme_path, id)
        else:
            # we don't have a local copy, use a worker thread to download it
            url = self.themes[scale][theme]['url']
            self.worker_start(self.plugin_dir, url, id)

    def worker_start(self, dir, url, id):
        """Start a worker instance on a background thread."""

        worker = NaturalEarthRasterWorker(dir, url, id)

        message_bar = self.iface.messageBar().createMessage('')

        label = QLabel('Downloading theme {}...'.format(id))
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        progress_bar = QProgressBar()
        progress_bar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        progress_bar.setMaximum(100)

        cancel_button = QPushButton()
        cancel_button.setText(self.tr('Cancel'))
        cancel_button.clicked.connect(worker.kill)

        message_bar.layout().addWidget(label)
        message_bar.layout().addWidget(progress_bar)
        message_bar.layout().addWidget(cancel_button)

        self.iface.messageBar().pushWidget(message_bar,
            self.iface.messageBar().INFO)
        self.message_bar = message_bar

        # start the worker in a new thread
        thread = QThread()
        worker.moveToThread(thread)

        # connect some odds and ends
        worker.finished.connect(self.worker_finished)
        worker.error.connect(self.worker_error)
        worker.progress.connect(progress_bar.setValue)
        thread.started.connect(worker.run)

        thread.start()

        self.thread = thread
        self.worker = worker

    def worker_finished(self, id):
        """Clean up after the worker and the thread."""

        # kill the thread
        self.worker.deleteLater()
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()

        # remove the progress bar
        self.iface.messageBar().popWidget(self.message_bar)

        if id is not None:
            # add the downloaded layer to the workspace
            path = os.path.join(self.plugin_dir, 'data', id, id + '.tif')
            self.add_raster_layer(path, id)
        else:
            # display an error message in the message bar
            message = self.tr('Theme download cancelled by user.')
            self.iface.messageBar().pushMessage(message,
                level=QgsMessageBar.INFO, duration=3)

    def worker_error(self, e, exception_string):
        """Handle errors from the worker thread."""

        # add the error message to the general log
        message = 'Worker thread exception: {}'.format(exception_string)
        QgsMessageLog.logMessage(message, level=QgsMessageLog.CRITICAL)

    def update_theme(self, index):
        """Update the theme selection combobox."""

        # remove all existing items from the combobox
        self.dialog.themeCombo.clear()

        # add items from the selected scale to the combobox
        scale = self.get_scale()
        for theme in self.themes[scale]:
            self.dialog.themeCombo.addItem(theme['name'])

    def update_preview(self, index):
        """Update the preview label image."""

        # get the filename of the preview image
        scale = self.get_scale()
        preview = self.themes[scale][index]['preview']

        # load the image
        path = os.path.join(self.plugin_dir, 'assets', 'previews', preview)
        image = QPixmap(path)

        # add the image to the label
        self.dialog.previewLabel.setPixmap(image)

    def add_raster_layer(self, path, id):
        """Add a downloaded raster layer to the workspace."""

        # create a new rasterlayer from the supplied TIF file
        layer = QgsRasterLayer(path, id)

        # load layer style based on number of bands
        bands = layer.bandCount()
        if bands == 1:
            path = os.path.join(self.plugin_dir, 'styles', 'singleband.qml')
        else:
            path = os.path.join(self.plugin_dir, 'styles', 'multiband.qml')

        layer.loadNamedStyle(path)

        # add the layer to the workspace
        QgsMapLayerRegistry.instance().addMapLayer(layer)

    def get_scale(self):
        """Get the name of a scale based on a combobox index."""

        index = self.dialog.scaleCombo.currentIndex()

        try:
            return ['high', 'medium', 'low'][index]
        except IndexError:
            return default

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Natural Earth Raster', message)
