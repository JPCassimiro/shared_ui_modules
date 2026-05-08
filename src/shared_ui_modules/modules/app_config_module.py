from PySide6.QtCore import QObject, QSettings
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator

from shared_ui_modules.modules.log_class import logger

from pathlib import Path

class AppConfigClass(QObject):
    # currentLangSignal = Signal(str)

    def __init__(self, parent = None):
        super().__init__()

        self.base_path_tr = Path("_internal/resources/translations")
        self.base_path_config = Path("_internal/resources/config/config.ini")

        self.settings = QSettings(str(self.base_path_config), QSettings.IniFormat)

        self.app_instance = QApplication.instance()
        
        self.language_list = [
            {"name":"Portugês","path":None},
            {"name":"English","path":"en_tr.qm"}
        ]
        
        self.current_translator = None
    
    def write_ini_file(self, property, value):
        self.settings.setValue(property, value)
        self.settings.sync()
        return self.settings.status()
            
    def change_language(self,file,name):
        print(f"change_language - file: {file}")
        status = None
        if file:
            file_path = self.base_path_tr / file
            self.write_ini_file("language_name", name)
            status = self.write_ini_file("language",str(file_path))
        else:
            self.write_ini_file("language_name", name)
            status = self.write_ini_file("language","None")

        if (status != None and status == QSettings.Status.NoError): #checks for error while updating settings
            language = self.settings.value("language")
            self.app_instance.removeTranslator(self.app_instance.translator)
            self.current_translator = QTranslator()
            if language and language != "None":
                self.app_instance.translator = self.current_translator
                self.app_instance.translator.load(language)
                self.app_instance.installTranslator(self.app_instance.translator)
                logger.debug("Língua alterada com sucesso")
        elif(status != None and status != QSettings.Status.NoError):
            logger.debug("Erro ao alterar língua")

    # def get_current_language(self):
    #     current_langauge = self.settings.value("Language")
    #     self.currentLangSignal.emit(current_langauge)
    
    # def change_language(self,file):
    #     app = QApplication.instance()

    #     if self.current_translator:
    #         app.removeTranslator(self.current_translator)
    #         self.current_translator = None

    #     if file:
    #         translator = QTranslator(app)
    #         file_path = self.base_path_tr / file
    #         res = translator.load(str(file_path))
    #         if res:
    #             self.current_translator = translator
    #             print(f"change_language res: {res} - self.current_translator: {self.current_translator}")

    # def write_config(self):