from shared_ui_modules.ui.views.log_modal_ui import Ui_logDialogForm

from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm
from shared_ui_modules.modules.log_class import logger

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QCoreApplication, QEvent

import datetime

class SharedLogModel(QDialog):
    def __init__(self,btSerialHandle: SharedBtSerialComm | None = None):
        super().__init__()
        
        #setup mshared modules
        self.btSerialHandle = btSerialHandle
        
        #ui setup
        self.ui = Ui_logDialogForm()
        self.ui.setupUi(self)
        
        self.translatable_strings = [
            QCoreApplication.translate("LoggerWidgetText","Janela de mensagens"),
            QCoreApplication.translate("LoggerWidgetText","Mensagem serial recebida do joystick:"),
            QCoreApplication.translate("LoggerWidgetText","Joystick não está conectado")
        ]
        
        self.setWindowTitle(self.translatable_strings[0])
        
        #get elements
        self.logTextEdit = self.ui.logTextEdit

        #setup connections
        self.btSerialHandle.mesReceivedSignal.connect(self.serial_message_append)
        self.btSerialHandle.log_modal_message.connect(self.serial_handle_message)

    def serial_handle_message(self,mes):
        try:
            logger.debug(f"serial_handle_message mes: {mes}")
            self.append_log(self.translatable_strings[mes])
        except Exception as e:
            logger.error(f"SharedLogModel serial_handle_message error: {e}")
        
    def serial_message_append(self,message):
        try:
            if message:
                self.append_log(f"{self.translatable_strings[1]} {message}")
        except Exception as e:
            logger.error(f"SharedLogModel serial_message_append error: {e}")

    def append_log(self,message):
        try:
            currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logTextEdit.appendPlainText(f"{currentDate}\n{message}\n")
        except Exception as e:
            logger.error(f"SharedLogModel append_log error: {e}")
        
    def clear_log(self):
        try:
            self.logTextEdit.clear()
        except Exception as e:
            logger.error(f"SharedLogModel clear_log error: {e}")

    def set_ui_texts(self):
        self.setWindowTitle(self.translatable_strings[0])
        
    def set_translatable_string(self):
        self.translatable_strings = [
            QCoreApplication.translate("LoggerWidgetText","Janela de mensagens"),
            QCoreApplication.translate("LoggerWidgetText","Mensagem serial recebida do joystick:")
        ]
    
    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.set_translatable_string()
            self.set_ui_texts()
            self.logTextEdit.clear()
        return super().changeEvent(event)