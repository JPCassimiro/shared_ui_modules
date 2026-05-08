from shared_ui_modules.ui.views.connected_device_item_ui import Ui_selectedDeviceForm

from PySide6.QtWidgets import QWidget

class ConnectedDeviceModel(QWidget):
    
    def __init__(self,deviceInfoDict):
        
        super().__init__()

        #setup ui
        self.ui = Ui_selectedDeviceForm()
        self.ui.setupUi(self)

        #get ui elements
        self.macLabel = self.ui.macLabel
        self.comPortLabel = self.ui.comPortLabel
        self.hidCheckLabel = self.ui.hidCheckLabel
        self.sppCheckLabel = self.ui.sppCheckLabel
        self.deviceIconLabel = self.ui.deviceIconLabel
        self.deviceNameLabel = self.ui.deviceNameLabel
        
        self.device_info_dict = deviceInfoDict
        
        self.hidCheckLabel.hide()
        self.sppCheckLabel.hide()
        self.comPortLabel.hide()
        # self.deviceIconLabel.hide()

        self.update_fields(deviceInfoDict)


    def update_fields(self,deviceInfoDict):
        self.macLabel.setText(deviceInfoDict["mac"])
        self.deviceNameLabel.setText(deviceInfoDict["name"])


        


    