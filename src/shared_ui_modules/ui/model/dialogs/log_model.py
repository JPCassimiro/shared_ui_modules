from shared_ui_modules.ui.views.log_modal_ui import Ui_logDialogForm
from PySide6.QtWidgets import QDialog
import datetime

class SharedLogModel(QDialog):
    def __init__(self):
        super().__init__()
        
        #ui setup
        self.ui = Ui_logDialogForm()
        self.ui.setupUi(self)
        
        
        self.setWindowTitle("Logger")
        
        #get elements
        self.logTextEdit = self.ui.logTextEdit

    def append_log(self,message):
        currentDate = datetime.datetime.now().strftime("%c")
        self.logTextEdit.appendPlainText(f"{currentDate}\n{message}\n")
        
    def clear_log(self):
        self.logTextEdit.clear()