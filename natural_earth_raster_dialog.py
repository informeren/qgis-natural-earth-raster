# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'natural_earth_raster_dialog.ui'
#
# Created: Thu Aug  6 11:55:27 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_NaturalEarthRasterDialog(object):
    def setupUi(self, NaturalEarthRasterDialog):
        NaturalEarthRasterDialog.setObjectName(_fromUtf8("NaturalEarthRasterDialog"))
        NaturalEarthRasterDialog.resize(340, 342)
        self.buttonBox = QtGui.QDialogButtonBox(NaturalEarthRasterDialog)
        self.buttonBox.setGeometry(QtCore.QRect(9, 306, 322, 27))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.scaleLabel = QtGui.QLabel(NaturalEarthRasterDialog)
        self.scaleLabel.setGeometry(QtCore.QRect(9, 9, 35, 17))
        self.scaleLabel.setObjectName(_fromUtf8("scaleLabel"))
        self.scaleCombo = QtGui.QComboBox(NaturalEarthRasterDialog)
        self.scaleCombo.setGeometry(QtCore.QRect(9, 32, 322, 27))
        self.scaleCombo.setObjectName(_fromUtf8("scaleCombo"))
        self.scaleCombo.addItem(_fromUtf8(""))
        self.scaleCombo.addItem(_fromUtf8(""))
        self.scaleCombo.addItem(_fromUtf8(""))
        self.themeLabel = QtGui.QLabel(NaturalEarthRasterDialog)
        self.themeLabel.setGeometry(QtCore.QRect(9, 65, 45, 17))
        self.themeLabel.setObjectName(_fromUtf8("themeLabel"))
        self.themeCombo = QtGui.QComboBox(NaturalEarthRasterDialog)
        self.themeCombo.setGeometry(QtCore.QRect(9, 88, 322, 27))
        self.themeCombo.setObjectName(_fromUtf8("themeCombo"))
        self.previewLabel = QtGui.QLabel(NaturalEarthRasterDialog)
        self.previewLabel.setGeometry(QtCore.QRect(10, 131, 320, 160))
        self.previewLabel.setFrameShape(QtGui.QFrame.Box)
        self.previewLabel.setText(_fromUtf8(""))
        self.previewLabel.setScaledContents(True)
        self.previewLabel.setObjectName(_fromUtf8("previewLabel"))

        self.retranslateUi(NaturalEarthRasterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NaturalEarthRasterDialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NaturalEarthRasterDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(NaturalEarthRasterDialog)

    def retranslateUi(self, NaturalEarthRasterDialog):
        NaturalEarthRasterDialog.setWindowTitle(_translate("NaturalEarthRasterDialog", "Dialog", None))
        self.scaleLabel.setText(_translate("NaturalEarthRasterDialog", "Scale:", None))
        self.scaleCombo.setItemText(0, _translate("NaturalEarthRasterDialog", "1:10m (large scale data, high resolution)", None))
        self.scaleCombo.setItemText(1, _translate("NaturalEarthRasterDialog", "1:10m (large scale data, medium resolution)", None))
        self.scaleCombo.setItemText(2, _translate("NaturalEarthRasterDialog", "1:50m (medium scale data, low resolution)", None))
        self.themeLabel.setText(_translate("NaturalEarthRasterDialog", "Theme:", None))


class NaturalEarthRasterDialog(QtGui.QDialog, Ui_NaturalEarthRasterDialog):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QDialog.__init__(self, parent, f)

        self.setupUi(self)

