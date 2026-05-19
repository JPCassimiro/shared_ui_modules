from PySide6.QtBluetooth import (QBluetoothLocalDevice, QBluetoothServiceDiscoveryAgent, QBluetoothServiceInfo,
                                 QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QLowEnergyController, QBluetoothSocket)
from PySide6.QtCore import QObject, Signal

from shared_ui_modules.modules.process_class import ProcessRunnerClass
from shared_ui_modules.modules.log_class import logger

target_device_name = "ESP32"#needs to be upper case for btpair, else use lower()
target_service_device_name = "esp32spp"
target_service = "rfcomm"

class BluetoothCommClass(QObject):
    hid_finish = Signal(str)
    hid_error = Signal()

    spp_finish = Signal(object)
    spp_error = Signal()
        
    le_finish = Signal(object)    
    le_error = Signal()
    
    local_error = Signal()
        
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.runner = ProcessRunnerClass()
        
        #local bluetooth device setup
        self.local_device = QBluetoothLocalDevice()

        #service discovery setup for esp32spp
        self.service_discovery = QBluetoothServiceDiscoveryAgent()
        # self.service_discovery.serviceDiscovered.connect(self.on_service_found)
        self.service_discovery.finished.connect(self.end_discovery)
        self.service_discovery.errorOccurred.connect(self.discovery_error)
        self.spp_service_list = []

        #device discovery setup for esp32 hid device
        self.discovery_agent = QBluetoothDeviceDiscoveryAgent()
        # self.discovery_agent.deviceDiscovered.connect(self.on_hid_device_found)
        self.discovery_agent.errorOccurred.connect(self.hid_discovery_error)
        self.discovery_agent.finished.connect(self.hid_discovery_end)
        self.hid_device_list = []

        #currently paired device
        self.paired_device = None
        
        #powered on device list
        self.powered_device_list = []

        #list of LE controllers for power check
        self.le_controller_list = []
        
        #unified list
        self.unified_list = []

        #local device pairing event finished handler 
        self.local_device.pairingFinished.connect(self.hid_pairEvent_finish)
        self.local_device.errorOccurred.connect(self.local_device_error)

        #process class run finish signal
        self.runner.processFinished.connect(self.process_run_finish)
        
        self.turn_local_device_on()
        
    def updated_device_handle(self,device,fields):
        logger.debug(f"updated_device_handle device:{device} - fields:{device.rssi()}")
        
    ############################ discovery functions ###############################    
    #appens bt serial services from available joysticks on a list
    # def on_service_found(self, service: QBluetoothServiceInfo):
    #     print(f"on_service_found: {service.serviceName().lower()}")
    #     # if(target_service_device_name in str(service.serviceName()).lower()):
    #     #     # self.desired_service = service
    #     #     self.spp_service_list.append(service)
            
    def spp_service_discovery(self):
        try:
            if not self.local_device:
                logger.debug("Adaptador bluetooth não encontrado")
                self.local_error.emit()

            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                logger.debug("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
                self.turn_local_device_on()
                self.local_error.emit()
            else:
                self.spp_service_list = []
                logger.debug("Começar descoberta por serviços")
                self.service_discovery.start()
        except Exception as e:
            logger.error(f"Erro ao começar descoberta de serviços bluetooth\nErr: {e}")
            self.local_error.emit()
            
    def end_discovery(self):
        discoveredServices = self.service_discovery.discoveredServices()
        logger.debug(f"end_discovery discoveredServices: {len(discoveredServices)}")
        sorted_list = sorted(discoveredServices,key=lambda s: s.device().address().toString())
        for service in sorted_list:
            if (target_service_device_name in str(service.serviceName()).lower()):
                self.spp_service_list.append(service)
        if any(self.spp_service_list):
            self.spp_finish.emit("spp")
        else:
            self.spp_finish.emit("spp")
            # self.spp_finish.emit()
            # self.toggle_bluetooth()
            # self.toggle_bluetooth()
        
    def discovery_error(self, error):
        logger.error("Erro na descoberta de serviços bluetooth\nErr: " + error)
        self.spp_error.emit()

    ############################ toggle functions ###############################    
    def toggle_bluetooth(self):
        try:
            if not self.local_device:
                self.local_error.emit()

            device_mode = self.local_device.hostMode() 
            
            if device_mode == QBluetoothLocalDevice.HostMode.HostConnectable:
                self.local_device.setHostMode(QBluetoothLocalDevice.HostMode.HostPoweredOff)
                self.local_error.emit()
                
            elif device_mode == QBluetoothLocalDevice.HostMode.HostPoweredOff:
                self.local_device.setHostMode(QBluetoothLocalDevice.HostMode.HostConnectable)
                self.local_error.emit()

            logger.debug("Sucesso em alterar o estado do adaptador bluetooth")
        except Exception as e:
            logger.error("Erro ao alterar o estado do adptador bluetooth\nErr: " + e)
         
         
    ############################ pair/unpair functions ###############################    
    def pair_device(self,serviceUuid,deviceMacString):
        try:
            if not self.local_device:
                logger.debug("Adaptador Bluetooth não encontrado")
                return
            
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                logger.debug("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
                self.turn_local_device_on()
            else:
                argumentList = ['-c','-s',f'{serviceUuid}','-b',f'{deviceMacString}']
                argStr = ["_internal/resources/bin/btcom.exe",argumentList]
                self.runner.run(argStr=argStr)
        except Exception as e:
            logger.debug(f"Erro no processo de conexão: {e}")
        
    def process_run_finish(self, object):
        try:
            if object["type"] == 0:#spp fallback case
                uuid_str = self.service_uuid_cleaner(object["message"],object["mac"])
                logger.debug(f"process_run_finish: {uuid_str}")
                self.spp_finish.emit({"mac":object["mac"],"uuid":uuid_str})
            else:
                self.spp_finish.emit("spp")
        except Exception as e:
            logger.debug(f"Erro no processo de conexão: {e}")
            self.spp_error.emit()
    
    def service_uuid_cleaner(self,str,mac_str):
        lines = str.splitlines()
        i = None
        for index, line in enumerate(lines):
            if mac_str in line:
                i = index
        if i != None:
            uuid_str = lines[i+1]
            start = uuid_str.find("{")+1
            end = uuid_str.find("}")
            return uuid_str[start:end]
        else:
            return None

    def unpair_device(self,deviceMacString):
        try:
            if not self.local_device:
                logger.debug("Adaptador Bluetooth não encontrado")
                return
            
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                logger.debug("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
                self.turn_local_device_on()
            else:
                argumentList = ['-u','-b',f'{deviceMacString}']
                argStr = ["_internal/resources/bin/btpair.exe",argumentList]
                self.runner.run(argStr=argStr)
        except Exception as e:
            logger.debug(f"Erro no processo de conexão: {e}")
            
    ############################ hid functions ###############################           
    def hid_device_discovery(self):
        try:
            if not self.local_device:
                logger.debug("Adaptador Bluetooth não encontrado")

            device_mode = self.local_device.hostMode() 

            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                logger.debug("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
                self.turn_local_device_on()
            else:
                logger.debug("Começar descoberta por dispositivos")
                # self.desired_service = None
                self.hid_device_list = []
                self.powered_device_list = []
                self.discovery_agent.start()
        except Exception as e:
            logger.error(f"Erro ao iniciar a descoberta de dispositivos: {e}")
        
    # def on_hid_device_found(self, device = QBluetoothDeviceInfo):
    #     if device.name().lower() == target_device_name.lower():
    #         logger.debug(f"on_hid_device_found device.rssi: {device.rssi()}")
        
    def hid_discovery_end(self):
        discoveredDevices = self.discovery_agent.discoveredDevices()
        sorted_list = sorted(discoveredDevices, key=lambda d: d.address().toString())
        for device in sorted_list:
            if device.name().lower() == target_device_name.lower():
                self.hid_device_list.append(device)
                #! testing lines
                # device_copy = QBluetoothDeviceInfo(device)
                # self.hid_device_list.append(device_copy)
                #! testing lines
        if any(self.hid_device_list):
            logger.debug(f"hid_discovery_end self.hid_device_list: {len(self.hid_device_list)}")
            self.hid_finish.emit("hid")
        else:
            self.hid_error.emit()

    def hid_device_pair(self,device):
        try:
            logger.debug(f"hid_device_pair device:{device.name()}")
            if device:
                self.local_device.requestPairing(device.address(), self.local_device.Pairing.Paired)
            else:
                logger.debug("Dispositivo não encontrado para o paremaneto")
        except Exception as e:
            logger.debug(f"Erro no processo de conexão: {e}")

    def hid_device_unpair(self,device):
        try:
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                logger.debug("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
                self.turn_local_device_on()
                self.hid_error.emit()
                return
            
            if device:
                logger.debug(f"hid_device_unpair {device.name()}")
                if self.local_device.pairingStatus(device.address()) == self.local_device.Pairing.AuthorizedPaired:
                    logger.debug(f"hid_device_unpair unpairing -> {device.name()}")
                    self.local_device.requestPairing(device.address(), self.local_device.Pairing.Unpaired)
                else:
                    self.hid_finish.emit("hid")
                    # logger.debug("Dispositivo não encontrado")
            elif self.paired_device:
                self.local_device.requestPairing(self.paired_device.address(), self.local_device.Pairing.Unpaired)
            else:
                logger.debug(f"hid_device_unpair variavel nula")
                self.hid_error.emit()
        except Exception as e:
                logger.debug(f"hid_device_unpair Erro no processo de desemparelhamento: {e}")
                self.hid_error.emit()

    def hid_discovery_error(self):
        logger.debug("Erro na descoberta de dispositivos HID")
        self.hid_error.emit()
            
    def hid_pairEvent_finish(self,address,pair):
        logger.debug(f"hid_pairEvent_finish address,pair:{address,pair}")
        try:
            self.hid_finish.emit("hid")
        except Exception as e:
            logger.debug(f"Erro no processo de conexão: {e}")
            self.hid_error.emit()

    def local_device_error(self):
        logger.debug(f"local_device_error")
        self.local_error.emit()

    #checks if the hid device connections status
    #!revise this function maybe?
    def check_device_connection(self,device):
        try:
            if device:
                logger.debug(f"hid_pairEvent_finish device true - self.local_device.pairingStatus(device.address()){self.local_device.pairingStatus(device.address())}")
                if self.local_device.pairingStatus(device.address()) == self.local_device.Pairing.AuthorizedPaired:
                    logger.debug("hid_pairEvent_finish device DEVICE PAIRED")
                    self.hid_finish.emit()
                else:
                    self.hid_finish.emit()
            elif self.paired_device:
                logger.debug(f"check_device_connection self.paired_device true")
                if self.local_device.pairingStatus(self.paired_device.address()) != self.local_device.Pairing.AuthorizedPaired:
                    self.hid_finish.emit("hid")
                else:
                    self.hid_error.emit()
            else:
                logger.debug(f"Dispositivo HID não encontrado")
                self.hid_error.emit()
        except Exception as e:
                # logger.debug(f"Erro no processo de emparelhamento de dispositivo")
                logger.debug(f"Erro no processo de emparelhamento de dispositivo: {e}")
                self.hid_error.emit()

    #check for currently paired device
    def turn_local_device_on(self):
        device_mode = self.local_device.hostMode() 
        if device_mode == QBluetoothLocalDevice.HostMode.HostPoweredOff:
            self.local_device.setHostMode(QBluetoothLocalDevice.HostMode.HostConnectable)

    ################################## LE Functions #################################
    def low_energy_check(self,device):
        try:
            logger.debug(f"BLuetoothCommClass low_energy_check device: {device}")
            #low energy controller setup for checking power state
            low_energy_controller = QLowEnergyController.createCentral(device)

            low_energy_controller.connected.connect(self.low_energy_connect_handle)
            low_energy_controller.errorOccurred.connect(self.low_energy_error_handle)

            self.le_controller_list.append(low_energy_controller)
            
            low_energy_controller.connectToDevice()
            
        except Exception as e:
            logger.debug(f"BLuetoothCommClass low_energy_check error: {e}")
            self.le_error.emit()
        
    def low_energy_error_handle(self,e):
        logger.debug(f"BLuetoothCommClass low_energy_error_handle error: {e}")
        self.le_finish.emit(None)

    def low_energy_connect_handle(self):
        self.le_finish.emit(self.sender().remoteAddress())
        
    def unpair_all_devices(self):
        try:
            if not self.local_device:
                logger.debug("Adaptador Bluetooth não encontrado")
                self.local_error.emit()
                return
            
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                logger.debug("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
                self.turn_local_device_on()
                self.local_error.emit()
            else:
                argumentList = ['-u']
                argStr = ["_internal/resources/bin/btpair.exe",argumentList]
                self.runner.run(argStr=argStr)
        except Exception as e:
            logger.debug(f"Erro no processo de conexão: {e}")
            self.local_error.emit()
            
    def spp_discovery_fallback(self,mac):
        try:
            if not self.local_device:
                logger.debug("Adaptador Bluetooth não encontrado")
                self.local_error.emit()
                return
            
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                logger.debug("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
                self.turn_local_device_on()
                self.local_error.emit()
            else:
                argumentList = ['-s"%sn%.%su%"','-n',f'{target_device_name}','-b',f'"({mac})"']
                argStr = ["_internal/resources/bin/btdiscovery.exe",argumentList]
                self.runner.run(argStr=argStr)
        except Exception as e:
            logger.debug(f"Erro no processo de conexão: {e}")
            self.local_error.emit()
            
    