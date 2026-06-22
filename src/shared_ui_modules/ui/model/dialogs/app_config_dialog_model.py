from shared_ui_modules.ui.views.app_config_modal_ui import Ui_AppConfigDialog

from shared_ui_modules.modules.release_watcher import ReleaseWatcherClass
from shared_ui_modules.modules.app_config_module import AppConfigClass
from shared_ui_modules.modules.log_class import logger

from PySide6.QtWidgets import QDialog, QMessageBox, QCheckBox
from PySide6.QtCore import QCoreApplication, Qt, QEvent, Signal

class SharedAppConfigModel(QDialog):

    def __init__(self):
        super().__init__()
        
        
        self.configModule = AppConfigClass()
        self.releaseWatcher = ReleaseWatcherClass(self.configModule)

        self.string_list_components = [
            QCoreApplication.translate("AppConfigDialogText","Configuração do aplicativo"),
            QCoreApplication.translate("MainMenuText","Aviso"),
            QCoreApplication.translate("MainMenuText","Nova versão da ferramenta.\nUse o botão de ajuda para encontrar o repositório!"),
            QCoreApplication.translate("MainMenuText","Parar de mostrar essa mensagem")
        ]

        #setup ui
        self.ui = Ui_AppConfigDialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        
        #get current langague
        self.current_language = self.configModule.settings.value("language_name")

        #get ui elements
        self.languageComboBox = self.ui.languageSelectionComboBox

        self.populate_language_comboBox()

        #setup connections
        self.languageComboBox.currentIndexChanged.connect(self.language_comboBox_change_handler)
        self.releaseWatcher.new_version.connect(self.new_version_handler)

        self.set_ui_text()

    def update_verification(self):
        try:
            self.releaseWatcher.get_allow_update()
            if self.releaseWatcher.allow_update != True:
                self.releaseWatcher.verification_handler()
        except Exception as e:
            logger.error(f"SharedAppConfigModel update_verification error: {e}")

    def get_api_endpoint(self):
        return

    def get_version_name(self):
        return

    def initialize_module(self):
        self.releaseWatcher.api_endpoint = self.get_api_endpoint()
        self.configModule.write_ini_file(self.configModule.version_name_property,self.get_version_name())
        self.releaseWatcher.return_api_request()
        self.update_verification()

    def set_ui_text(self):
        self.setWindowTitle(self.string_list_components[0])
            
    def language_comboBox_change_handler(self):
        try:
            self.select_language()
        except Exception as e:
            logger.error(f"SharedAppConfigModel language_comboBox_change_handler error: {e}")

    def select_language(self):
        try:
            self.configModule.change_language(self.languageComboBox.currentData(),self.languageComboBox.currentText())
        except Exception as e:
            logger.error(f"SharedAppConfigModel select_language error: {e}")
            raise

    def populate_language_comboBox(self):
        try:
            self.languageComboBox.clear() 
            current_index = -1
            if self.configModule.language_list:
                for i,l in enumerate(self.configModule.language_list):
                    self.languageComboBox.addItem(l["name"],l["path"])
                    if self.current_language == l["name"]:
                        current_index = i
                self.languageComboBox.setCurrentIndex(current_index)    
        except Exception as e:
            logger.error(f"SharedAppConfigModel populate_language_comboBox error: {e}")
            
    def new_version_handler(self):
        try:
            logger.debug(f"SharedMainMenu new_version_handler")
            warning = QMessageBox(self)
            warning.setWindowTitle(self.string_list_components[1])
            warning.setText(self.string_list_components[2])
            cb = QCheckBox(self.string_list_components[3],warning)
            warning.setCheckBox(cb)
            warning.setWindowModality(Qt.ApplicationModal)
            warning.exec()
            if cb.isChecked():
                self.block_update_message()
        except Exception as e:
            logger.error(f"SharedAppConfigModel new_version_handler error: {e}")

    def block_update_message(self):
        try:
            self.configModule.write_ini_file(self.configModule.update_message_property,"True")
        except Exception as e:
            logger.error(f"SharedAppConfigModel block_update_message error: {e}")
            raise

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.string_list_components = [
                QCoreApplication.translate("AppConfigDialogText","Configuração do aplicativo"),
                QCoreApplication.translate("MainMenuText","Aviso"),
                QCoreApplication.translate("MainMenuText","Nova versão da ferramenta.\nUse o botão de ajuda para encontrar o repositório!"),
                QCoreApplication.translate("MainMenuText","Parar de mostrar essa mensagem")
                ]
            self.set_ui_text()
        return super().changeEvent(event)
        