from PySide6.QtBluetooth import (QBluetoothLocalDevice, QBluetoothServiceDiscoveryAgent, QBluetoothServiceInfo,
                                 QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QLowEnergyController, QBluetoothSocket)
from PySide6.QtCore import QObject, Signal, QProcess

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
            if self.local_device is None:
                raise Exception("Adaptador bluetooth não encontrado")

            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                self.turn_local_device_on()
                raise Exception("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
            else:
                self.spp_service_list = []
                logger.debug("Começar descoberta por serviços")
                self.service_discovery.start()
        except Exception as e:
            logger.error(f"BluetoothCommClass spp_service_discovery error: {e}")
            self.local_error.emit()
            
    def end_discovery(self):
        discoveredServices = self.service_discovery.discoveredServices()
        logger.debug(f"end_discovery discoveredServices: {len(discoveredServices)}")
        sorted_list = sorted(discoveredServices,key=lambda s: s.device().address().toString())
        #!testing lines ↓ 
        # sorted_list = []
        #!testing lines ↑
        for service in sorted_list:
            if (target_service_device_name in str(service.serviceName()).lower()):
                self.spp_service_list.append(service)
        self.spp_finish.emit("spp")
        
    def discovery_error(self, e):
        logger.error(f"BluetoothCommClass discovery_error error: {e}")
        self.spp_error.emit()

    ############################ toggle functions ###############################    
    def toggle_bluetooth(self):
        try:
            if self.local_device is None:
                raise Exception("Adaptador bluetooth não encontrado")

            device_mode = self.local_device.hostMode() 
            
            if device_mode == QBluetoothLocalDevice.HostMode.HostConnectable:
                self.local_device.setHostMode(QBluetoothLocalDevice.HostMode.HostPoweredOff)
                
            elif device_mode == QBluetoothLocalDevice.HostMode.HostPoweredOff:
                self.local_device.setHostMode(QBluetoothLocalDevice.HostMode.HostConnectable)

            self.local_error.emit()
            logger.debug("Sucesso em alterar o estado do adaptador bluetooth")
        except Exception as e:
            logger.error(f"BluetoothCommClass toggle_bluetooth error: {e}")
            self.local_error.emit()

    ############################ pair/unpair functions ###############################    
    def pair_device(self,serviceUuid,deviceMacString):
        try:
            if self.local_device is None:
                raise Exception("Adaptador bluetooth não encontrado")
            
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                self.turn_local_device_on()
                raise Exception("Adaptador bluetooth esta desligado. Tentado ligar o adaptador...")
            else:
                argumentList = ['-c','-s',f'{serviceUuid}','-b',f'{deviceMacString}']
                argStr = ["_internal/resources/bin/btcom.exe",argumentList]
                self.runner.run(argStr=argStr)
        except Exception as e:
            logger.error(f"BluetoothCommClass pair_device error: {e}")
        
    def process_run_finish(self, processEndDict):
        try:
            if processEndDict["status"] == True:
                if processEndDict["type"] == "btdiscovery.exe":#spp fallback case
                    uuid_str = self.service_uuid_cleaner(processEndDict["message"],processEndDict["mac"])
                    logger.debug(f"process_run_finish: {uuid_str}")
                    self.spp_finish.emit({"mac":processEndDict["mac"],"uuid":uuid_str})
                elif processEndDict["type"] == "btpair.exe" or processEndDict["type"] == "btdiscovery":
                    self.spp_finish.emit("spp")
            else:
                if processEndDict["status"] == False:
                    if processEndDict["type"] == "btdiscovery.exe":
                        self.spp_finish.emit({"mac":processEndDict["mac"],"uuid":None})
                    elif processEndDict["type"] == "btpair.exe" or processEndDict["type"] == "btdiscovery":
                        self.spp_finish.emit("spp")
        except Exception as e:
            logger.error(f"BluetoothCommClass process_run_finish error: {e}")
            self.spp_error.emit()
    
    def service_uuid_cleaner(self,str,mac_str):
        try:
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
        except Exception as e:
            logger.error(f"BluetoothCommClass service_uuid_cleaner error: {e}")

    def unpair_device(self,deviceMacString):
        try:
            if self.local_device is None:
                raise Exception("Adaptador Bluetooth não encontrado")
            
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                self.turn_local_device_on()
                raise Exception("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
            else:
                argumentList = ['-u','-b',f'{deviceMacString}']
                argStr = ["_internal/resources/bin/btpair.exe",argumentList]
                self.runner.run(argStr=argStr)
        except Exception as e:
            logger.error(f"BluetoothCommClass service_uuid_cleaner error: {e}")
            
    ############################ hid functions ###############################           
    def hid_device_discovery(self):
        try:
            if self.local_device is None:
                raise Exception("Adaptador Bluetooth não encontrado")

            device_mode = self.local_device.hostMode() 

            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                self.turn_local_device_on()
                raise Exception("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
            else:
                logger.debug("Começar descoberta por dispositivos")
                # self.desired_service = None
                self.hid_device_list = []
                self.powered_device_list = []
                self.discovery_agent.start()
        except Exception as e:
            logger.error(f"BluetoothCommClass hid_device_discovery error: {e}")
        
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

    def hid_device_pair(self,device):
        try:
            logger.debug(f"hid_device_pair device:{device.name()}")
            if device:
                self.local_device.requestPairing(device.address(), self.local_device.Pairing.Paired)
            else:
                raise Exception("device not found")
        except Exception as e:
            logger.error(f"BluetoothCommClass hid_device_pair error: {e}")

    def hid_device_unpair(self,device):
        try:
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                self.turn_local_device_on()
                raise Exception("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
            
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
                raise Exception("null device")
        except Exception as e:
                logger.error(f"BluetoothCmmClass hid_device_unpair error: {e}")
                self.hid_error.emit()

    def hid_discovery_error(self,e):
        logger.error(f"BluetoothCmmClass hid_discovery_error: {e}")
        self.hid_error.emit()
            
    def hid_pairEvent_finish(self,address,pair):
        logger.debug(f"hid_pairEvent_finish address,pair:{address,pair}")
        try:
            self.hid_finish.emit("hid")
        except Exception as e:
            logger.error(f"BluetoothCmmClass hid_pairEvent_finish error: {e}")
            self.hid_error.emit()

    def local_device_error(self,e):
        logger.error(f"BluetoothCmmClass local_device_error error: {e}")
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
                    raise Exception(f"check_device_error")
            else:
                raise Exception(f"Dispositivo HID não encontrado")
        except Exception as e:
                logger.error(f"BluetoothCommClass check_device_connection error: {e}")
                self.hid_error.emit()

    #check for currently paired device
    def turn_local_device_on(self):
        try:
            device_mode = self.local_device.hostMode() 
            if device_mode == QBluetoothLocalDevice.HostMode.HostPoweredOff:
                self.local_device.setHostMode(QBluetoothLocalDevice.HostMode.HostConnectable)
        except Exception as e:
            logger.error(f"BluetoothCommClass turn_local_device_on error: {e}")

    ################################## LE Functions #################################
    def low_energy_check(self,device):
        try:
            logger.debug(f"BluetoothCommClass low_energy_check device: {device}")
            #low energy controller setup for checking power state
            low_energy_controller = QLowEnergyController.createCentral(device)

            low_energy_controller.connected.connect(self.low_energy_connect_handle)
            low_energy_controller.errorOccurred.connect(self.low_energy_error_handle)

            self.le_controller_list.append(low_energy_controller)
            
            low_energy_controller.connectToDevice()
            
        except Exception as e:
            logger.error(f"BluetoothCommClass low_energy_check error: {e}")
            self.le_error.emit()
        
    def low_energy_error_handle(self,e):
        logger.error(f"BluetoothCommClass low_energy_error_handle error: {e}")
        self.le_finish.emit(None)

    def low_energy_connect_handle(self):
        try:
            self.le_finish.emit(self.sender().remoteAddress())
        except Exception as e:
            logger.error(f"BluetoothCommClass low_energy_connect_handle error: {e}")
        
    def unpair_all_devices(self):
        try:
            if self.local_device is None:
                raise Exception("Adaptador Bluetooth não encontrado")
            
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                self.turn_local_device_on()
                raise Exception("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
            else:
                argumentList = ['-u']
                argStr = ["_internal/resources/bin/btpair.exe",argumentList]
                self.runner.run(argStr=argStr)
        except Exception as e:
            logger.error(f"BluetoothCommClass unpair_all_devices error: {e}")
            self.local_error.emit()
            
    #tells process class to trigger btdiscovery with desired mac and target device name
    def spp_discovery_fallback(self,mac):
        try:
            if self.local_device is None:
                raise Exception("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
            
            device_mode = self.local_device.hostMode() 
            
            if device_mode != QBluetoothLocalDevice.HostMode.HostConnectable:
                self.turn_local_device_on()
                raise Exception("Adaptador Bluetooth esta desligado. Tentado ligar o adaptador...")
            else:
                argumentList = ['-s"%sn%.%su%"','-n',f'{target_device_name}','-b',f'"({mac})"']
                argStr = ["_internal/resources/bin/btdiscovery.exe",argumentList]
                self.runner.run(argStr=argStr)
        except Exception as e:
            logger.error(f"BluetoothCommClass spp_discovery_fallback error: {e}")
            self.local_error.emit()

    def stop_all_processes(self):
        try:
            def on_disc():
                all_disconnected = all(
                    c.state() != QLowEnergyController.ControllerState.ConnectedState or QLowEnergyController.ControllerState.ConnectingState
                    for c in self.le_controller_list
                )
                if all_disconnected:
                    self.le_controller_list = []
            
            if self.discovery_agent.isActive() == True:
                self.discovery_agent.stop()
            
            if self.service_discovery.isActive() == True:
                self.service_discovery.stop()

            for controller in self.le_controller_list[:]:
                if controller.state() == QLowEnergyController.ControllerState.ConnectedState or QLowEnergyController.ControllerState.ConnectingState:
                    controller.disconnected(on_disc)
                    controller.disconnectFromDevice()
                    
            if self.runner.p.state() != QProcess.NotRunning:
                self.runner.p.kill()
        except Exception as e:
            logger.error(f"BluetoothCommClass stop_all_process error: {e}")
            raise
        