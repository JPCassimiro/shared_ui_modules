from shared_ui_modules.ui.views.app_helper_modal_ui import Ui_appHelpDialog

from shared_ui_modules.modules.desktop_services import DekstopServicesClass
from shared_ui_modules.modules.log_class import logger

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QCoreApplication, QEvent

from pathlib import Path

class SharedAppHelperModel(QDialog):
    def __init__(self):
        
        super().__init__()

        self.string_list_components = [
            QCoreApplication.translate("AppHelperDialogText","Ajuda"),
            QCoreApplication.translate("AppHelperDialogText","<a href='_internal/manual/manual.html'>Manual de usuário<a/>"),#has to be updated on linguist too
        ]

        self.repo_string = None
        
        self.ui = Ui_appHelpDialog()
        self.ui.setupUi(self)

        #get ui elements
        self.manualLinkLabel = self.ui.manualLinkLabel
        self.githubLinkLabel = self.ui.githubLinkLabel

        #setup connections
        self.manualLinkLabel.linkActivated.connect(self.open_manual)

        self.setWindowModality(Qt.ApplicationModal)

    def get_repo_string(self):
        return

    def initialize_module(self):
        self.repo_string = self.get_repo_string()
        self.string_list_components.append(self.repo_string)
        self.set_ui_text()

    def open_manual(self,filePath):
        try:
            self.file_path = Path(filePath)
            DekstopServicesClass().open_folder(self.file_path)
        except Exception as e:
            logger.error(f"SharedAppHelperModel open_manual error: {e}")

    def set_ui_text(self):
        try:
            self.setWindowTitle(self.string_list_components[0])
            self.manualLinkLabel.setText(self.string_list_components[1])
            self.githubLinkLabel.setText(self.string_list_components[2])
        except Exception as e:
            logger.error(f"SharedAppHelperModel set_ui_text error: {e}")
            
    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.string_list_components = [
                QCoreApplication.translate("AppHelperDialogText","Ajuda"),
                QCoreApplication.translate("AppHelperDialogText","<a href='_internal/manual/manual.html'>Manual de usuário<a/>"),#has to be updated on linguist too
            ]
            self.string_list_components.append(self.repo_string)
            self.set_ui_text()
        return super().changeEvent(event)