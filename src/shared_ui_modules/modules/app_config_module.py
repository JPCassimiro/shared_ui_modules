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
        
        self.update_message_property = "block_update_message"
        self.version_name_property = "ver"

        self.current_translator = None
    
    def write_ini_file(self, property, value):
        try:
            self.settings.setValue(property, value)
            self.settings.sync()
            return self.settings.status()
        except Exception as e:
            logger.error(f"AppConfigClass write_ini_file error: {e}")
            
    def get_property(self,property):
        try:
            prop = self.settings.value(property)
            return prop
        except Exception as e:
            logger.error(f"AppConfigClass get_property error: {e}")
            
    def change_language(self,file,name):
        try:
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
                raise Exception("language swap error")
        except Exception as e:
            logger.error(f"AppConfigClass change_language error: {e}")