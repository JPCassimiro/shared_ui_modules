from shared_ui_modules.ui.views.end_config_modal_ui import Ui_endConfigModalDialog
from shared_ui_modules.modules.log_class import logger

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QCoreApplication, QEvent


class SharedEndConfigModel(QDialog):
    
    def __init__(self):
        super().__init__()
        
        #setup translatable strins
        self.string_list_components = [
            QCoreApplication.translate("EndConfigDialogText","Finalizado"),
        ]

        self.string_list_messages = [
            QCoreApplication.translate("EndConfigDialogText","Erro ao configurar um atributo, refaça a configuração."),
            QCoreApplication.translate("EndConfigDialogText","Atributos configurados com sucesso!")
        ]
        
        self.ui = Ui_endConfigModalDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(self.string_list_components[0])
        
        #set up variables
        self._recieved_messages = []
        self.sent_message_total = 0

        #get ui elements
        self.messageField = self.ui.messageField 

        self.finished.connect(self.finished_handler)
    
    @property
    def recieved_messages(self):
        return self._recieved_messages
    
    @recieved_messages.setter
    def recieved_messages(self,message):
        self._recieved_messages.append(message)
        if self.sent_message_total:
            if len(self._recieved_messages) == self.sent_message_total:
                self.finish_message()
    
    def finish_message(self):
        try:
            logger.debug(f"EndConfigModel finish_message self.sent_message_total:{self.sent_message_total}")
            if self.sent_message_total:
                if sum(self._recieved_messages) != self.sent_message_total:
                    self.messageField.append(self.string_list_messages[0])
                else:
                    self.messageField.append(self.string_list_messages[1])
                self._recieved_messages = []
                self.sent_message_total = 0
        except Exception as e:
            logger.error(f"SharedEndConfigModel finish_message error: {e}")

    def set_ui_text(self):
        self.setWindowTitle(self.string_list_components[0])

    def recieve_end_message(self,message):
        try:
            logger.debug(f"recieve_end_message message:{message}")
            if("N" in message):
                self.recieved_messages = False
                # self.messageField.append(self.string_list_messages[0])
                # logger.debug(f"Erro ao configurar atributo")
            else:
                self.recieved_messages = True
                # self.messageField.append(self.string_list_messages[1])
                # logger.debug(f"Atributo configurado com sucesso")
        except Exception as e:
            logger.error(f"SharedEndConfigModel recieve_end_message error: {e}")

    def finished_handler(self):
        self.messageField.clear()

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.string_list_components = [
                QCoreApplication.translate("EndConfigDialogText","Finalizado"),
            ]
            self.set_ui_text()
        return super().changeEvent(event)