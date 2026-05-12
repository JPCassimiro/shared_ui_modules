from shared_ui_modules.modules.log_class import logger

from PySide6.QtCore import QObject, Signal

import requests

class ReleaseWatcherClass(QObject):
    
    new_version = Signal()
    
    def __init__(self, configModule, parent = None):
        super().__init__()

        self.configModule = configModule

        self.req_json = None
        self.latest_name = None
        self.current_name = None
        self.allow_update = None
        
        self.api_endpoint = None

        self.get_allow_update()

    def return_api_request(self):
        try:
            req = requests.get(self.api_endpoint)
            if req:
                self.req_json = req.json()
        except Exception as e:   
            logger.error(f"ReleaseWatcherClass error: {e}")                 

    def get_current_name(self):
        ver = self.configModule.get_property(self.configModule.version_name_property)
        if ver:
            self.current_name = ver

    def get_latets_name(self):
        if self.req_json:
            self.latest_name = self.req_json["name"]
    
    def check_version_diference(self):
        if self.current_name != self.latest_name:
            logger.debug(f"diferent version!")
            self.new_version.emit()
        else:
            logger.debug(f"same version!")

    def get_allow_update(self):
        self.allow_update = bool(self.configModule.get_property(self.configModule.update_message_property))
      
    def verification_handler(self):
        self.get_current_name()
        self.get_latets_name()
        self.check_version_diference()