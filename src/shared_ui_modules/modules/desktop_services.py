from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl, QObject

from shared_ui_modules.modules.log_class import logger

class DekstopServicesClass(QObject):
    
    def __init__(self, parent = None):

        super().__init__(parent)

        self.deskServ = QDesktopServices()

    def open_folder(self, folderPath):
        try:
            url = QUrl.fromLocalFile(folderPath)

            if not url:
                raise Exception("null url")

            self.deskServ.openUrl(url)
            
        except Exception as e:
            logger.error(f"DekstopServicesClass open_folder error: {e}")