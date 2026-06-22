from PySide6.QtWidgets import QWidget

class SharedConfigWidgetModel(QWidget):
    def __init__(self, btSerialHandle, LogModel):
        super().__init__()

    def message_normalization(self,p,action):
        try:
            if not p or not action:
                raise Exception(f"null p or action: {p},{action}")
            
            valueStr = ""
            if(p < 10):#value always needs to be sent in a 3 digit format 
                valueStr = f"00{p}"
            elif(p < 100):
                valueStr = f"0{p}"
            else:
                valueStr = f"{p}"
            message = "*M{}{}".format(action,valueStr)
            #when sending the serial message, action index start at 1
            return message
        except Exception as e:
            logger.error(f"ConfigWidgetModel message_normalization error: {e}")
            raise

    def confirm_button_handler(self):
        try:
            self.start_config_process()
        except Exception as e:
            logger.error(f"SharedConfigWidgetModel confirm_button_handler error: {e}")

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