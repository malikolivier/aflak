import datetime
import os
import sys

from pyqtgraph.Qt import QtCore


QtCore.QCoreApplication.setOrganizationName('aflak')
QtCore.QCoreApplication.setOrganizationDomain('aflak.jp')
QtCore.QCoreApplication.setApplicationName('aflak')


class Settings:
    settings = QtCore.QSettings()

    @classmethod
    def addRecentFile(cls, filePath):
        files = cls.settings.value('RecentFiles')
        if type(files) is not list:
            files = []
        absolutePath = os.path.join(os.getcwd(), filePath)
        files = [f for f in files if f['path'] != absolutePath]
        files.append({
            'time': datetime.datetime.now(),
            'path': absolutePath
        })
        cls.settings.setValue('RecentFiles', files)

    @classmethod
    def getRecentFiles(cls):
        files = cls.settings.value('RecentFiles')
        if type(files) is not list:
            return []
        else:
            try:
                files = sorted(files, key=lambda f: f['time'], reverse=True)
                return [f['path'] for f in files]
            except TypeError as e:
                # In case memory on disk got corrupted, reset memory
                print('Unexpected error on parsing RecentFiles',
                      file=sys.stderr)
                print(e, file=sys.stderr)
                cls.clearRecentFiles()
                return []

    @classmethod
    def clearRecentFiles(cls):
        cls.settings.setValue('RecentFiles', [])
