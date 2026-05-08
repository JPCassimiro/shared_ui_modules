from shared_ui_modules.ui.views.connection_manager_ui import Ui_loggerForm

from shared_ui_modules.modules.bluetooth_comunication import BluetoothCommClass
from shared_ui_modules.modules.log_class import logger
# from modules.json_writer import JsonWriterClass
from shared_ui_modules.modules.connection_manager_state_machine import (IdleState, DisconnectionState, 
                                                      ErrorState, ConnectionState, FindPortState, DeviceSearchState)

from shared_ui_modules.ui.model.components.listed_device_item_model import ListedDeviceItemModel
from shared_ui_modules.ui.model.components.connected_device_item_model import ConnectedDeviceModel

from PySide6.QtWidgets import QWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtStateMachine import QStateMachine

#basic widget funcionalitty
    #list all available joysticks
    #allow joystick connection using button
    #conncetion 
        #disconnect currently connected joystikc
        #connect new joystick

class SharedConnectionManagerModel(QWidget):

    sideMenuDisableSignal = Signal(bool)
    to_idle = Signal()
    confirmed_conn_loss = Signal()

    def __init__(self,  logModel, serialBtClass):

        super().__init__()


        #modules setup
        self.bluetoothHandle = BluetoothCommClass()
        self.serialBtClass = serialBtClass
        self.logModel = logModel
        
        #setup ui
        self.ui = Ui_loggerForm()
        self.ui.setupUi(self)

        #get ui elements
        self.pairDeviceButton = self.ui.pairDeviceButton
        self.reloadListButton = self.ui.reloadListButton
        self.unpairDeviceButton = self.ui.unpairDeviceButton
        self.deviceListWidget = self.ui.deviceListWidget
        self.deviceContainer = self.ui.deviceContainer
        self.deviceContainerFrame = self.ui.deviceContainerFrame
        
        #variable setup
        self.selected_device = [None,None]#0: device 1: service
        self._selected_list_item = None
        self._connected_device_watcher = False

        #connection setup_selected_device
        self.deviceListWidget.clicked.connect(self.device_select_handle)
        self.pairDeviceButton.clicked.connect(self.pair_selected_device)
        # self.serialBtClass.port_finish.connect(self.successful_pair)
        # self.serialHandleClass.port_finish.connect(self.successful_pair)
        self.unpairDeviceButton.clicked.connect(self.full_unpair)
        
        self.selected_list_item = None
        self.connected_device_watcher = False

        self.state_machine_init()

    def conn_lost_check(self):
        if self.connected_device_watcher == True:
            #device has been unexpectedly disconnected 
                #show modal
                #formally disconnect device
            self.machine.full_pair = False
            self.confirmed_conn_loss.emit()

    def device_container_style_change(self):
        if self._connected_device_watcher == False:
            self.deviceContainerFrame.setStyleSheet("""background-color: #353231;""")
        else:
            self.deviceContainerFrame.setStyleSheet("""background-color: #F89E59;""")

    def get_json_writer(self):
        return

    def setup_module(self):
        self.jsonWriter = self.get_json_writer()

    @property
    def selected_list_item(self):
        return self._selected_list_item

    @selected_list_item.setter
    def selected_list_item(self, index):
        self._selected_list_item = index
        self.pair_button_state_watcher()
        
    def pair_button_state_watcher(self):
        if self._selected_list_item != None:
            self.pairDeviceButton.setEnabled(True)
        else:
            self.pairDeviceButton.setEnabled(False)

    @property
    def connected_device_watcher(self):
        return self._connected_device_watcher
    
    @connected_device_watcher.setter
    def connected_device_watcher(self, state):
        self._connected_device_watcher = state
        self.unpair_device_button_watcher()

    def unpair_device_button_watcher(self):
        if self._connected_device_watcher:
            self.unpairDeviceButton.setEnabled(True)
        else:
            self.unpairDeviceButton.setEnabled(False)
        self.device_container_style_change()

    #clears every relevant variable, releses ui and clears list
    def nuke_screen_on_error(self):
        self.selected_device = [None, None]
        self.deviceListWidget.clear()
        self.service_search_in_progress = False
        self.device_search_in_progress = False
        self.selected_list_item = None

    #full pair error fallback
    def handle_process_ending_error(self,message):
        self.logModel.append_log(message)
        logger.error(message)
        self.nuke_screen_on_error()
        self.to_idle.emit()

    # to garantee button state consistency, both pair and unpair button get called on disable and enable screen,
    #controlVal parameter gets passed se we block unpair device even when the variable is not null
    def disable_screen(self, pairControl = True, unpairControl = True):
        self.pairDeviceButton.setEnabled(False)
        self.unpairDeviceButton.setEnabled(False)
        self.reloadListButton.setEnabled(False)
        self.deviceListWidget.setEnabled(False)
        self.sideMenuDisableSignal.emit(False)
        
    def release_screen(self):
        # for button in self.ui.windowContainer.findChildren(QPushButton):
        #     button.setEnabled(True)
        self.pairDeviceButton.setEnabled(True)
        self.unpairDeviceButton.setEnabled(True)
        self.reloadListButton.setEnabled(True)
        self.deviceListWidget.setEnabled(True)
        self.pair_button_state_watcher()
        self.unpair_device_button_watcher()
        self.sideMenuDisableSignal.emit(True)
        
    #adds connected device widget to the layout
    def show_connected_device(self):
        #generete device info dict
        deviceInfoDict = {
            "mac": self.selected_device[0].address().toString(),
            "name": self.selected_device[0].name(),
            "hid_device": self.selected_device[0],
        }
        #create device item
        self.connected_item = ConnectedDeviceModel(deviceInfoDict)
        self.deviceContainer.layout().addWidget(self.connected_item)
        self.connected_device_watcher = True

    #clears port addr and mac
    # def clear_serial_info(self):
    #     self.serialHandleClass.clear_serial_info()

    #gets info from the currently selected device from the list and updates self.selected_device
    def device_select_handle(self, index):
        item = self.sender().item(index.row())
        widget = self.sender().itemWidget(item)
        if widget.isEnabled():
            device_id = widget.deviceDict["id"]
            service_uuid = widget.deviceDict["uuid"]
            self.selected_device[0] = self.bluetoothHandle.hid_device_list[device_id]
            self.selected_device[1] = service_uuid
            self.machine.selected_device = self.selected_device
            self.selected_list_item = index.row()
            self.logModel.append_log(f"Dispositivo selecionado: {self._selected_list_item+1}")
            logger.debug(f"device_select_handle self.selected_device: {self.selected_device}")

    #checks for selected devices and starts the full pair
    def pair_selected_device(self):
        if self.selected_device[0] and self.selected_device[1]:
            self.logModel.append_log("Emparelhando dispositivo selecionado, aguarde...")
            self.machine.full_pair = True
            
    #gets device addr            
    def end_full_pair(self,addr = None):
        logger.debug(f"end_full_pair addr:{addr}")
        try:
            self.successful_pair()
        except Exception as e:
            self.handle_process_ending_error(f"Erro ao encontrar dispositivos\nErro: {e}")

    #will recive the signal from serial handle that indicates if the port was found successfully
    def port_found_signal(self,signal):
        if signal == True:
            self.successful_pair()
        elif signal == False:
            self.handle_process_ending_error("Erro ao tentar obter porta serial do joystick")

    def successful_pair(self):
        self.jsonWriter.write_devices(deviceDict={"mac":self.selected_device[0].address().toString().lower(),"uuid":self.selected_device[1],"name":self.selected_device[0].name()})
        self.show_connected_device()
        item = self.deviceListWidget.takeItem(self._selected_list_item)
        del item
        self.bluetoothHandle.paired_device = self.selected_device[0]
        self.selected_device = [None,None]
        self.selected_list_item = None
        self.logModel.append_log("Sucesso no emparelhamento")
        self.serialBtClass.conn_lost.connect(self.conn_lost_check)
        
    def full_unpair(self):
        self.logModel.append_log("Desemparelhando dispositivo, aguarde...")
        self.machine.full_pair = False
           
    def unpair_finish_handler(self):
        logger.debug(f"unpair_finish_handler")
        # self.clear_serial_info()
        self.selected_device = [None,None]
        self.connected_item.deleteLater()
        self.selected_list_item = None
        self.bluetoothHandle.paired_device = None
        self.connected_device_watcher = False
        self.logModel.append_log("Sucesso no desemparelhamento")
        self.to_idle.emit()
        
    #visually updates the list and atributes deviceDict to each item
    def update_list(self):
        try:
            
            self.deviceListWidget.clear()
            
            for i, listed_device_dict in enumerate(self.bluetoothHandle.unified_list):
                if self.bluetoothHandle.paired_device == None or self.bluetoothHandle.paired_device.address() != listed_device_dict["device"].address(): 

                    deviceDict = {
                        "listName": i+1,
                        "name": listed_device_dict["device"].name(),
                        "mac": listed_device_dict["device"].address().toString(),
                        "id": i,
                        "turned_on": listed_device_dict["turned_on"],
                        "uuid": listed_device_dict["service"]
                    }
                    
                    logger.debug(f"update_list deviceDict:{deviceDict}")

                    item = ListedDeviceItemModel(deviceDict)
                    item_container = QListWidgetItem(self.deviceListWidget)
                    item_container.setSizeHint(item.sizeHint())
                    
                    if deviceDict["turned_on"] == False:
                        item_container.setFlags(item_container.flags() & ~(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
                        item.setEnabled(False)
                        
                    self.deviceListWidget.addItem(item_container)
                    self.deviceListWidget.setItemWidget(item_container,item)
                    
        except IndexError as e:
            logger.debug(f"index out of range error")
        except Exception as e:
            logger.debug(f"update_list error: {e}")
            self.bluetoothHandle.spp_error.emit()#force error state
            
    def index_out_of_range_handler(self):
        self.bluetoothHandle.spp_error.connect(self.index_out_of_range_finish)
        self.bluetoothHandle.spp_finish.connect(self.index_out_of_range_finish)
        self.disable_screen()
        self.bluetoothHandle.unpair_all_devices()

    def index_out_of_range_finish(self):
        self.bluetoothHandle.spp_error.disconnect(self.index_out_of_range_finish)
        self.bluetoothHandle.spp_finish.disconnect(self.index_out_of_range_finish)
        self.handle_process_ending_error(f"Erro na busca de dispositivos, é possivel que este erro tenha sido causado pela conexão do serviço SPP, conecte e desconecte o dispostivo SPP manualmente para garantir")
        
    def cached_device_check(self,mac_str):
        try:
            logger.debug(f"cached_device_check mac_str: {mac_str}")
            data = self.jsonWriter.read_json_file("_internal/resources/cached_devices/cached_devices.json")
            if data:
                if data[mac_str]:
                    device_data = data[mac_str]
                    return device_data["uuid"]
                else:
                    return None
        except Exception as e:
            logger.debug(f"cached_device_check error: {e}")
        
    def state_machine_init(self):
        self.machine = QStateMachine()
        
        self.idle_state = IdleState(self.machine, self.bluetoothHandle,functions = {
            "release_screen": self.release_screen,
            "disable_screen": self.disable_screen
        })
        self.search_state = DeviceSearchState(self.machine, self.bluetoothHandle, functions = self.cached_device_check, logModel= self.logModel)
        self.disconnect_state = DisconnectionState(self.machine, self.bluetoothHandle, self.serialBtClass, functions = {
            "conn_lost_check": self.conn_lost_check
        })
        self.error_state = ErrorState(self.machine, self.bluetoothHandle, functions = {
            "handle_process_ending_error": self.handle_process_ending_error
        })
        self.connection_state = ConnectionState(self.machine, self.bluetoothHandle, self.serialBtClass)
        self.find_port_state = FindPortState(self.machine, self.bluetoothHandle, self.serialBtClass)

        #idle state transitions
        self.idle_state.addTransition(self.pairDeviceButton.clicked, self.disconnect_state)
        self.idle_state.addTransition(self.unpairDeviceButton.clicked, self.disconnect_state)
        self.idle_state.addTransition(self.reloadListButton.clicked, self.search_state)
        self.idle_state.addTransition(self.confirmed_conn_loss, self.disconnect_state)
        
        #search state transitions
        self.search_state.addTransition(self.search_state.search_end, self.idle_state)
        self.search_state.addTransition(self.bluetoothHandle.hid_error, self.error_state)
        self.search_state.addTransition(self.bluetoothHandle.spp_error, self.error_state)
        self.search_state.addTransition(self.bluetoothHandle.le_error, self.error_state)
        self.search_state.addTransition(self.bluetoothHandle.local_error, self.error_state)

        #disconnect state transitions
        self.disconnect_state.addTransition(self.to_idle, self.idle_state)
        self.disconnect_state.addTransition(self.disconnect_state.conn_start, self.connection_state)
        self.disconnect_state.addTransition(self.bluetoothHandle.hid_error, self.error_state)
        self.disconnect_state.addTransition(self.bluetoothHandle.spp_error, self.error_state)
        self.disconnect_state.addTransition(self.bluetoothHandle.local_error, self.error_state)

        #error state transitions
        self.error_state.addTransition(self.to_idle, self.idle_state)

        #connection state transtions
        self.connection_state.addTransition(self.connection_state.conn_finish, self.find_port_state)
        self.connection_state.addTransition(self.bluetoothHandle.spp_error, self.error_state)
        self.connection_state.addTransition(self.bluetoothHandle.hid_error, self.error_state)
        self.connection_state.addTransition(self.bluetoothHandle.local_error, self.error_state)

        #find_port state transitions
        self.find_port_state.addTransition(self.find_port_state.pair_success, self.idle_state)
        self.find_port_state.addTransition(self.serialBtClass.port_error, self.error_state)
        # self.find_port_state.addTransition(self.serialHandleClass.port_finish, self.idle_state)
        # self.find_port_state.addTransition(self.serialHandleClass.port_error, self.error_state)

        self.machine.setInitialState(self.idle_state)
        
        #shared variables
        self.machine.selected_device = None
        self.machine.addr = None
        self.machine.spp_watcher = None
        self.machine.hid_watcher = None
        self.machine.full_pair = None
        self.machine.search = None

        #signal connection to ui
        self.find_port_state.pair_success.connect(self.end_full_pair)
        self.disconnect_state.disc_finish.connect(self.unpair_finish_handler)
        self.search_state.search_end.connect(self.update_list)
        
        self.machine.start()
                
    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
        return super().changeEvent(event)
