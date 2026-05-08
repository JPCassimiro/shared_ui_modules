from PySide6.QtWidgets import QWidget

class SharedConfigWidgetModel(QWidget):
    def __init__(self, btSerialHandle, LogModel):
        super().__init__()

    def repeat_button_handler(self):
        if self.sender().objectName() == "repeatOffButton":
            self.param_select.update({"repeat_key":False})
        else:
            self.param_select.update({"repeat_key":True})

    def message_received_handler(self,response):
        self.end_modal.recieve_end_message(response)

    def send_serial_message(self,message):
        if self.btSerialHandle.bt_socket != None:
            # self.serialHandleClass.open_port()
            self.btSerialHandle.send_message(message)
            # self.serialHandleClass.send_message(message)
        
    def arrow_text_conversion(self,key):#chages literal word for directional arrows to icons
        key_text = key
        if key == "UP":
            key_text = str("↑")
        elif key == "DOWN":
            key_text = str("↓")
        elif key == "LEFT":
            key_text = str("←")
        elif key == "RIGHT":
            key_text = str("→")
        return key_text