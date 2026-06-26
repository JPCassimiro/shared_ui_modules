from PySide6.QtWidgets import QPushButton, QMainWindow, QApplication, QMessageBox, QCheckBox
from PySide6.QtCore import QEvent, QCoreApplication, Qt, Signal

from shared_ui_modules.modules.log_class import logger

class SharedMainMenuWindow(QMainWindow):    
    def __init__(self):
        super().__init__()

        self.main_menu_dialog_string_list = [
            QCoreApplication.translate("MainMenuText","Erro de conexão com o joystick"),
            QCoreApplication.translate("MainMenuText","A conexão com o joystick foi perdida, realizando desemparelhamento"),
            QCoreApplication.translate("MainMenuText","Joystick não está conectado")
        ]

    def initialize_module(self):
        self.logModalButton.clicked.connect(self.log_button_handler)
        self.appConfigButton.clicked.connect(self.app_config_button_handler)
        self.manualButton.clicked.connect(self.app_manual_button_handler)

        #bt connection error signal conn
        self.connection_manager_widget.confirmed_conn_loss.connect(self.conn_loss_dialog_handle)
        self.btSerialHandle.port_error.connect(self.no_connection_dialog_handle)

    def therapist_select_handler(self,infoDict):
        try:
            if infoDict is None:
                raise Exception(f"null infoDict: {infoDict}")
            self.title_widget.info_dict = infoDict.copy()
            self.title_widget.update_fields()
        except Exception as e:
            logger.error(f"SharedMainMenuWindow therapist_select_handler error: {e}")
        
    def patient_select_handler(self,infoDict):
        try:
            if infoDict is None:
                raise Exception(f"null infoDict: {infoDict}")
            
            self.patient_widget.info_dict = infoDict.copy()
            self.patient_widget.update_fields()
            if "id" in infoDict:
                self.user_stats_widget.assing_user(infoDict["id"],infoDict["name"])
                self.config_widget.current_user = infoDict["id"]
                self.game_profile_widget.assing_user(infoDict["id"])
        except Exception as e:
            logger.error(f"SharedMainMenuWindow patient_select_handler error: {e}")
            
    def log_button_handler(self):
        self.logModel.open()
        self.logModel.raise_()
        self.logModel.activateWindow()

    # toggles side menu buttons accordingly
    def side_menu_button_toggler(self, clicked_button):
        try:
            for button in self.side_menu.findChildren(QPushButton):
                if button != clicked_button:
                    button.setEnabled(True)
                else:
                    clicked_button.setEnabled(False)
        except Exception as e:
            logger.error(f"SharedMainMenuWindow side_menu_button_toggler error: {e}")
                
    def side_menu_button_disabler(self, state, clicked_button):
        try:
            for button in self.side_menu.findChildren(QPushButton):
                if button == clicked_button:
                    clicked_button.setEnabled(False)
                else:
                    button.setEnabled(state)
            self.appConfigButton.setEnabled(state)
        except Exception as e:
            logger.error(f"SharedMainMenuWindow side_menu_button_toggler error: {e}")
        
    def app_config_button_handler(self):
        self.appConfigModal.show()

    def app_manual_button_handler(self):
        self.manual_modal.show()

    def to_config_signal_handle(self,config):
        try:
            if config is None:
                raise Exception(f"null config: {config}")
            self.config_widget.assing_card_values(config)
            self.stackedWidget.setCurrentIndex(1)
            self.side_menu_button_toggler(self.configButton)
        except Exception as e:
            logger.error(f"SharedMainMenuWindow to_config_signal_handle error: {e}")

    def conn_loss_dialog_handle(self):
        try:
            self.stackedWidget.setCurrentIndex(0)
            warning = QMessageBox(self)
            warning.setWindowTitle(self.main_menu_dialog_string_list[0])
            warning.setText(self.main_menu_dialog_string_list[1])
            warning.setWindowModality(Qt.ApplicationModal)
            warning.show()
        except Exception as e:
            logger.error(f"SharedMainMenuWindow conn_loss_dialog_handle error: {e}")

    def no_connection_dialog_handle(self):
        try:
            warning = QMessageBox(self)
            warning.setWindowTitle(self.main_menu_dialog_string_list[0])
            warning.setText(self.main_menu_dialog_string_list[2])
            warning.setWindowModality(Qt.ApplicationModal)
            warning.show()
        except Exception as e:
            logger.error(f"SharedMainMenuWindow no_connection_dialog_handle error: {e}")
        
    # event override    
    def closeEvent(self, event):
        modal_list = []
        modal_list.append(QApplication.activeModalWidget())
        if any(modal_list):
            for m in modal_list:
                m.close()
        return super().closeEvent(event)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.main_menu_dialog_string_list = [
                QCoreApplication.translate("MainMenuText","Erro de conexão com o joystick"),
                QCoreApplication.translate("MainMenuText","A conexão com o joystick foi perdida, realizando desemparelhamento"),
                QCoreApplication.translate("MainMenuText","Joystick não está conectado")
            ]
            self.ui.retranslateUi(self)
        return super().changeEvent(event)
        