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
        self.releaseWatcher.get_allow_update()
        if self.releaseWatcher.allow_update != True:
            self.releaseWatcher.verification_handler()

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
        self.select_language()

    def select_language(self):
        print(f"{self.sender().objectName()} - {self.sender().currentIndex()}")        
        self.configModule.change_language(self.languageComboBox.currentData(),self.languageComboBox.currentText())

    def populate_language_comboBox(self):
        self.languageComboBox.clear() 
        current_index = -1
        if self.configModule.language_list:
            for i,l in enumerate(self.configModule.language_list):
                self.languageComboBox.addItem(l["name"],l["path"])
                if self.current_language == l["name"]:
                    current_index = i
            self.languageComboBox.setCurrentIndex(current_index)    
    
    def new_version_handler(self):
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

    def block_update_message(self):
        self.configModule.write_ini_file(self.configModule.update_message_property,"True")

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
        