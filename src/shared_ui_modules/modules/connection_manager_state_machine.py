from shared_ui_modules.modules.log_class import logger

from PySide6.QtStateMachine import QState
from PySide6.QtCore import Signal

class IdleState(QState):
    def __init__(self, machine, bluetoothHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoothHandle
        self.functions = functions
        
    def onEntry(self, event):
        logger.debug("IdleState onEntry")
        self.functions["release_screen"]()
        self.machine.spp_watcher = False
        self.machine.hid_watcher = False
        return super().onEntry(event)

    def onExit(self, event):
        logger.debug("IdleState onExit")
        self.functions["disable_screen"](pairControl=False)
        return super().onExit(event)

#has to deal with 3 diferrent cases:
    #full pair a new device
    #full unpair a paired device
    #unpair a device connected device and pair a new device
class DisconnectionState(QState):

    disc_finish = Signal()
    conn_start = Signal()

    def __init__(self, machine, bluetoothHandle, btSerialHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoothHandle
        self.btSerialHandle = btSerialHandle
        self.functions = functions
        self.sp_case = None
        self.spp_counter = 0
        self.hid_counter = 0

    def onEntry(self, event):
        logger.debug("DisconnectionState onEntry")
        self.btSerialHandle.conn_lost.disconnect(self.functions["conn_lost_check"])
        self.btHandle.spp_finish.connect(self.handle_finish)
        self.btHandle.hid_finish.connect(self.handle_finish)

        res = self.case_evaluation()
        logger.debug(f"DisconncetionState onEntry res:{res}")
        match(res):
            case 0:
                logger.debug(f"DisconnectionState case 0")
                self.btHandle.hid_device_unpair(self.btHandle.paired_device)
                self.btHandle.unpair_device(self.btHandle.paired_device.address().toString().lower())
                self.btSerialHandle.clear_socket() 
            case 1:
                logger.debug(f"DisconnectionState case 1")
                self.btHandle.hid_device_unpair(self.machine.selected_device[0])
                self.btHandle.unpair_device(self.machine.selected_device[0].address().toString().lower())   
            case 2:
                logger.debug(f"DisconnectionState case 2")
                self.sp_case = True
                self.btHandle.hid_device_unpair(self.btHandle.paired_device)
                self.btHandle.unpair_device(self.btHandle.paired_device.address().toString().lower())
                self.btHandle.hid_device_unpair(self.machine.selected_device[0])
                self.btHandle.unpair_device(self.machine.selected_device[0].address().toString().lower())  
                self.btSerialHandle.clear_socket() 

        return super().onEntry(event)

    def onExit(self, event):
        logger.debug("DisconnectionState onExit")
        self.machine.full_pair = None
        self.sp_case = None
        self.spp_counter = 0
        self.hid_counter = 0
        return super().onExit(event)
    
    def handle_finish(self, status):
        if self.sp_case == True:
            res = self.sp_case_async_check(status)
        else:
            res = self.async_check(status)
        logger.debug(f"DisconnectionState handle_finish res:{res}")
        if res == "disc_finish":
            logger.debug(f"DisconnectionState handle_finish disc_finish")
            self.conn_check()
        elif res == "conn_start":
            logger.debug(f"DisconnectionState handle_finish conn_start")
            self.btHandle.spp_finish.disconnect(self.handle_finish)
            self.btHandle.hid_finish.disconnect(self.handle_finish)
            self.conn_start.emit()
            
    def sp_case_async_check(self, status):
        if status == "hid":
            self.hid_counter += 1
        elif status == "spp":
            self.spp_counter += 1
        if self.spp_counter == 2 and self.hid_counter == 2:
            return "conn_start"

    def case_evaluation(self):
        #full unpair case
        if self.machine.selected_device[0] == None and self.btHandle.paired_device:
            return 0
        #full pair case
        elif self.machine.selected_device[0] and self.btHandle.paired_device == None:
            return 1
        #connected device and full pair case
        elif self.machine.selected_device[0] and self.btHandle.paired_device:
            return 2

    def conn_check(self):
        def finish_send(status):
            logger.debug(f"DisconnectionState conn_check")
            self.btHandle.hid_finish.disconnect(finish_send)
            self.disc_finish.emit()
        
        self.btHandle.hid_finish.disconnect(self.handle_finish)
        self.btHandle.spp_finish.disconnect(self.handle_finish)
        self.btHandle.hid_finish.connect(finish_send)
        self.btHandle.check_device_connection(self.machine.selected_device[0])

    def async_check(self,status):
        if status == "spp":
           self.machine.spp_watcher = True
        if status == "hid":
            self.machine.hid_watcher = True
        if self.machine.hid_watcher  == True and self.machine.spp_watcher == True:
            self.machine.spp_watcher = False
            self.machine.hid_watcher = False
            logger.debug(f"async_check successfull")
            logger.debug(f"async_check full_pair:{self.machine.full_pair}")
            if self.machine.full_pair != None:
                if self.machine.full_pair == True:
                    return "conn_start"
                else:
                    return "disc_finish"
    
class ErrorState(QState):
    def __init__(self, machine, bluetoohHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoohHandle
        self.functions = functions
        
    def onEntry(self, event):
        logger.debug(f"ErrorState onEntry")
        self.functions["handle_process_ending_error"]("Erro no processo de conexão!")
        return super().onEntry(event)

    def onExit(self, event):
        logger.debug(f"ErrorState onExit")
        return super().onExit(event)

class ConnectionState(QState):
    
    conn_finish = Signal()
    
    def __init__(self, machine, bluetoohHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoohHandle
        self.functions = functions
        
    def onEntry(self, event):
        logger.debug("ConnectionState onEntry")
        # self.btHandle.spp_finish.connect(self.handle_finish)
        self.btHandle.hid_finish.connect(self.handle_finish)
        if self.machine.selected_device:
            self.btHandle.hid_device_pair(self.machine.selected_device[0])
        return super().onEntry(event)

    def onExit(self, event):
        logger.debug("ConnectionState onExit")
        # self.btHandle.spp_finish.disconnect(self.handle_finish)
        self.btHandle.hid_finish.disconnect(self.handle_finish)
        return super().onExit(event)

    def handle_finish(self, status):
        res = self.async_check(status)

        if res == "conn_finish":
            self.machine.addr = self.machine.selected_device[0].address().toString().replace(":","").lower()
            self.conn_finish.emit()
            
    def async_check(self,status):
        if status == "hid":
            return "conn_finish"

class DeviceSearchState(QState):
    
    search_end = Signal()
    fallback_finish = Signal(object)
    
    def __init__(self, machine, bluetoohHandle, functions = None, logModel = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoohHandle
        self.functions = functions
        self.device_counter = 0
        self.logModel = logModel
        self.pending_callbacks = {}

    def onEntry(self, event):
        logger.debug("DeviceSearchState onEntry")
        self.logModel.append_log("Procurando por dispositivos, aguarde...")
        self.device_counter = 0
        self.machine.search = True
        self.btHandle.unified_list = []
        self.btHandle.spp_finish.connect(self.handle_finish)
        self.btHandle.hid_finish.connect(self.handle_finish)
        self.btHandle.le_finish.connect(self.handle_power_finish)
        self.fallback_finish.connect(self.fallback_return_result)
        self.btHandle.hid_device_discovery()
        self.btHandle.spp_service_discovery()
        return super().onEntry(event)

    def onExit(self, event):
        logger.debug("DeviceSearchState onExit")
        self.btHandle.spp_finish.disconnect(self.handle_finish)
        self.btHandle.hid_finish.disconnect(self.handle_finish)
        self.btHandle.le_finish.disconnect(self.handle_power_finish)
        self.fallback_finish.disconnect(self.fallback_return_result)
        self.machine.search = None
        self.pending_callbacks = {}
        return super().onExit(event)

    def handle_finish(self, status):
        res = self.async_check(status)

        if res == "search_end":
            self.device_power_check()

    def device_power_check(self):
        self.device_counter = len(self.btHandle.hid_device_list)
        logger.debug(f"DeviceSearchState device_power_check self.device_counter:{self.device_counter}")
        if self.device_counter > 0:
            for device in self.btHandle.hid_device_list:
                self.btHandle.low_energy_check(device)
    
    def handle_power_finish(self, res):
        logger.debug(f"DeviceSearchState handle_power_finish res:{res}")
        if res:
            self.device_counter -= 1
            self.btHandle.powered_device_list.append(res)
        else:
            self.device_counter -= 1

        if self.device_counter == 0:
            for controller in self.btHandle.le_controller_list:
                self.clear_le_controller(controller)
            
    def clear_le_controller(self,controller):
        def on_disc():
            controller.deleteLater()
            self.btHandle.le_controller_list.pop(self.btHandle.le_controller_list.index(controller))
            if len(self.btHandle.le_controller_list) == 0:
                self.btHandle.unified_list = self.unify_list()
                logger.debug(f"clear_le_controller self.btHandle.unified_list: {self.btHandle.unified_list}")
                self.service_null_check()

        controller.disconnected.connect(on_disc)
        controller.disconnectFromDevice()
        
    def unify_list(self):
        dict_list = []
        
        service_map = {
            service.device().address().toString(): service
            for service in self.btHandle.spp_service_list
        }
        
        powered_device_map = set(self.btHandle.powered_device_list)
        
        for device in self.btHandle.hid_device_list:
            d = {
                "device": device,
                "turned_on": False,
                "service": None,
            }
            
            if any(powered_device_map):
                if device.address() in powered_device_map:
                    d["turned_on"] = True
            
            if device.address().toString() in service_map:
                d["service"] = service_map[device.address().toString()].serviceUuid().toString()
            
            dict_list.append(d)

        return dict_list 

    def spp_fallback(self,mac_str):
        self.btHandle.spp_finish.connect(self.spp_fallback_finish_handle)
        self.btHandle.spp_discovery_fallback(mac_str)
            
    def spp_fallback_finish_handle(self,message):
        self.btHandle.spp_finish.disconnect(self.spp_fallback_finish_handle)
        if len(message) >= 2:
            self.fallback_finish.emit(message)
            
    def cached_check(self,mac_str):
        logger.debug(f"cached_check mac_str: {mac_str}")
        uuid_str = self.functions(mac_str.lower())
        if uuid_str:
            return uuid_str
        else:
            return None

    def service_null_check(self):
        try:
            counter = False
            for device_dict in self.btHandle.unified_list:
                if device_dict["service"] == None and device_dict["turned_on"] == True:
                    mac_str = device_dict["device"].address().toString()
                    uuid_str = self.cached_check(mac_str)
                    if uuid_str:
                        device_dict["service"] = uuid_str
                    else:
                        self.pending_callbacks[mac_str] = device_dict
                        self.spp_fallback(mac_str)
                        counter = True
            if counter == False:
                logger.debug(f"service_null_check success")
                self.search_end.emit()
        except Exception as e:
            logger.debug(f"service_null_check error: {e}")
            
    def fallback_return_result(self, message):
        if message["mac"] in self.pending_callbacks:
            device_dict = self.pending_callbacks.pop(message["mac"])
            device_dict["service"] = message["uuid"]
            
            if not self.pending_callbacks:
                self.search_end.emit()
    
    def async_check(self, status):
        logger.debug(f"SharedStateMachine async_check status: {status}")
        if status == "hid":
            self.machine.hid_watcher = True
        if status == "spp":
            self.machine.spp_watcher = True
           
        if self.machine.spp_watcher == True and self.machine.hid_watcher == True:
            self.machine.spp_watcher = False 
            self.machine.hid_watcher = False
            logger.debug(f"SharedStateMachine async_check success")
            if self.machine.search:
                return "search_end"

class FindPortState(QState):

    pair_success = Signal(str)

    def __init__(self, machine, bluetoohHandle, btSerialHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoohHandle
        self.btSerialHandle = btSerialHandle
        self.functions = functions

    def onEntry(self, event):
        logger.debug(f"FindPortState onEntry")
        if self.machine.addr:
            logger.debug(f"FindPortState self.machine.addr:{self.machine.addr}")
            self.btSerialHandle.port_finish.connect(self.on_socket_sucess)
            self.btSerialHandle.create_service_socket(self.machine.selected_device[0].address(),self.machine.selected_device[1])
        return super().onEntry(event)

    def onExit(self, event):
        logger.debug(f"FindPortState onExit")
        self.btHandle.paired_device = self.machine.selected_device[0]
        self.machine.selected_device = [None, None]
        self.machine.addr = None
        self.btSerialHandle.port_finish.disconnect(self.on_socket_sucess)
        return super().onExit(event)

    def on_socket_sucess(self):
        self.pair_success.emit(self.machine.addr)
        