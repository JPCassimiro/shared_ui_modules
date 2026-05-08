from shared_ui_modules.ui.views.app_config_modal_ui import Ui_AppConfigDialog

from shared_ui_modules.modules.app_config_module import AppConfigClass

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QCoreApplication, Qt, QEvent

class SharedAppConfigModel(QDialog):
    def __init__(self):
        super().__init__()

        self.string_list_components = [
            QCoreApplication.translate("AppConfigDialogText","Configuração do aplicativo")
        ]

        #setup ui
        self.ui = Ui_AppConfigDialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        

        self.appConfigInstance = AppConfigClass()

        #get current langague
        self.current_language = self.appConfigInstance.settings.value("language_name")

        #get ui elements
        self.languageComboBox = self.ui.languageSelectionComboBox

        self.populate_language_comboBox()

        #setup connections
        self.languageComboBox.currentIndexChanged.connect(self.language_comboBox_change_handler)


        self.set_ui_text()


    def set_ui_text(self):
        self.setWindowTitle(self.string_list_components[0])
            

    def language_comboBox_change_handler(self):
        self.select_language()

    def select_language(self):
        print(f"{self.sender().objectName()} - {self.sender().currentIndex()}")        
        self.appConfigInstance.change_language(self.languageComboBox.currentData(),self.languageComboBox.currentText())

    def populate_language_comboBox(self):
        self.languageComboBox.clear() 
        current_index = -1
        if self.appConfigInstance.language_list:
            for i,l in enumerate(self.appConfigInstance.language_list):
                self.languageComboBox.addItem(l["name"],l["path"])
                if self.current_language == l["name"]:
                    current_index = i
            self.languageComboBox.setCurrentIndex(current_index)    
    
    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.string_list_components = [
                QCoreApplication.translate("AppConfigDialogText","Configuração do aplicativo")
            ]
            self.set_ui_text()
        return super().changeEvent(event)
        