from shared_ui_modules.ui.views.listed_device_item_ui import Ui_listedDeviceForm
from shared_ui_modules.modules.log_class import logger

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QEvent, QCoreApplication
from PySide6.QtBluetooth import QBluetoothUuid
from PySide6.QtCore import QUuid

class ListedDeviceItemModel(QWidget):
    

    def __init__(self, deviceDict: dict):
        
        super().__init__()

        #ui setup
        self.ui = Ui_listedDeviceForm()
        self.ui.setupUi(self)

        #get ui elements
        self.listedDeviceNameLabel = self.ui.listedDeviceNameLabel
        self.listedDeviceIconLabel = self.ui.listedDeviceIconLabel
        self.listedDeviceAddressLabel = self.ui.listedDeviceAddressLabel
        
        self.listedDeviceIconLabel.hide()

        self.deviceDict = deviceDict
        if type(self.deviceDict["uuid"]) == str: 
            uuid = QUuid(self.deviceDict["uuid"])
            self.deviceDict["uuid"] = QBluetoothUuid(uuid)
        # self.deviceDict["name"]    
        # self.deviceDict["mac"]
        # self.deviceDict["listName"]
        # self.deviceDict["id"]
        # self.deviceDict["uuid"]
        # self.deviceDict["turned_on"]
        
        self.set_texts()
        
    def set_texts(self):
        try:
            device_satus = QCoreApplication.translate("DeviceText","Desligado")
            device_name =  QCoreApplication.translate("DeviceText","Dispositivo {num}")
            device_name = device_name.format(num = self.deviceDict["listName"])
            self.listedDeviceAddressLabel.setText(self.deviceDict["mac"])
            self.listedDeviceNameLabel.setText(device_name if self.deviceDict["turned_on"] == True else f"{device_name} - {device_satus}")
        except Exception as e:
            logger.error(f"ListedDeviceItemModel set_texts error: {e}")

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.set_texts()
        return super().changeEvent(event)
        
        