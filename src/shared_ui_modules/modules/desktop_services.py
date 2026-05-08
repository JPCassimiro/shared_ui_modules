from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl, QObject

class DekstopServicesClass(QObject):
    
    def __init__(self, parent = None):

        super().__init__(parent)

        self.deskServ = QDesktopServices()

    def open_folder(self, folderPath):
        try:
            url = QUrl.fromLocalFile(folderPath)
            self.deskServ.openUrl(url)
            
        except Exception as e:
            print(f"Erro ao abrir link: {e}")