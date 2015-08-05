from PyQt4.QtCore import pyqtSignal, QObject

import os.path
import tempfile
import traceback
import urllib2
import zipfile


class NaturalEarthRasterWorker(QObject):
    """Background worker which downloads and unpacks Natural Earth data."""

    finished = pyqtSignal(object)
    error = pyqtSignal(Exception, basestring)
    progress = pyqtSignal(float)

    def __init__(self, dir, url, id):
        """Constructor."""
        QObject.__init__(self)

        self.dir = dir
        self.url = url
        self.id = id

        self.killed = False

    def run(self):
        """Download the selected theme from the Natural Earth CDN."""

        ret = None

        try:
            # create temporary file for storing the downloaded .zip archive
            temp_file = tempfile.TemporaryFile()

            # start the request and set a reasonable chunk size (64kB)
            request = urllib2.urlopen(self.url)
            chunk_size = 64 * 1024

            # get the size of the archive for use with the progress bar
            content_length = int(request.headers['content-length'])

            downloaded = 0
            with temp_file:
                for chunk in iter(lambda: request.read(chunk_size), ''):
                    if self.killed is True:
                        break
                    if not chunk:
                        break

                    temp_file.write(chunk)

                    # update the progress bar
                    downloaded += chunk_size
                    percentage = downloaded / float(content_length) * 100
                    self.progress.emit(percentage)

                # try to unpack the downloaded .zip archive in the plugin dir
                path = os.path.join(self.dir, 'data')
                with zipfile.ZipFile(temp_file, 'r') as zip:
                    zip.extractall(path)
                    ret = self.id

        except Exception, e:
            self.error.emit(e, traceback.format_exc())

        self.finished.emit(ret)

    def kill(self):
        """Ask the worker thread to terminate."""

        self.killed = True
