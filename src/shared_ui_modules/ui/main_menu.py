from PySide6.QtWidgets import QPushButton, QMainWindow, QApplication, QMessageBox
from PySide6.QtCore import QEvent, QCoreApplication, Qt

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
        self.title_widget.info_dict = infoDict.copy()
        self.title_widget.update_fields()
        
    def patient_select_handler(self,infoDict):
        self.patient_widget.info_dict = infoDict.copy()
        self.patient_widget.update_fields()
        if "id" in infoDict:
            self.user_stats_widget.assing_user(infoDict["id"],infoDict["name"])
            self.config_widget.current_user = infoDict["id"]
            self.game_profile_widget.assing_user(infoDict["id"])
            
    def log_button_handler(self):
        self.logModel.open()

    # toggles side menu buttons accordingly
    def side_menu_button_toggler(self, clicked_button):
        for button in self.side_menu.findChildren(QPushButton):
            if button != clicked_button:
                button.setEnabled(True)
            else:
                clicked_button.setEnabled(False)
                
    def side_menu_button_disabler(self, state, clicked_button):
        for button in self.side_menu.findChildren(QPushButton):
            if button == clicked_button:
                clicked_button.setEnabled(False)
            else:
                button.setEnabled(state)
        self.appConfigButton.setEnabled(state)
        
    def app_config_button_handler(self):
        self.appConfigModal.show()

    def app_manual_button_handler(self):
        self.manual_modal.show()

    def to_config_signal_handle(self,config):
        self.config_widget.assing_card_values(config)
        self.stackedWidget.setCurrentIndex(1)
        self.side_menu_button_toggler(self.configButton)

    def conn_loss_dialog_handle(self):
        warning = QMessageBox(self)
        warning.setWindowTitle(self.main_menu_dialog_string_list[0])
        warning.setText(QCoreApplication.translate(self.main_menu_dialog_string_list[1]))
        warning.setWindowModality(Qt.ApplicationModal)
        warning.show()
        self.stackedWidget.setCurrentIndex(0)

    def no_connection_dialog_handle(self):
        warning = QMessageBox(self)
        warning.setWindowTitle(self.main_menu_dialog_string_list[0])
        warning.setText(self.main_menu_dialog_string_list[2])
        warning.setWindowModality(Qt.ApplicationModal)
        warning.show()
        
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
        