from shared_ui_modules.ui.views.connection_manager_ui import Ui_loggerForm

from shared_ui_modules.modules.bluetooth_comunication import BluetoothCommClass
from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm
from shared_ui_modules.modules.log_class import logger
# from modules.json_writer import JsonWriterClass
from shared_ui_modules.modules.connection_manager_state_machine import (IdleState, DisconnectionState, 
                                                      ErrorState, ConnectionState, FindPortState, DeviceSearchState)

from shared_ui_modules.ui.model.components.listed_device_item_model import ListedDeviceItemModel
from shared_ui_modules.ui.model.components.connected_device_item_model import ConnectedDeviceModel
from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel

from PySide6.QtWidgets import QWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal, QEvent, QCoreApplication
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

    def __init__(self,  logModel: SharedLogModel | None, serialBtClass: SharedBtSerialComm | None):

        super().__init__()

        self.logger_window_translatable_strings = [
            QCoreApplication.translate("LoggerWidgetText","Dispositivo selecionado:"),
            QCoreApplication.translate("LoggerWidgetText","Emparelhando dispositivo selecionado, aguarde..."),
            QCoreApplication.translate("LoggerWidgetText","Sucesso no emparelhamento"),
            QCoreApplication.translate("LoggerWidgetText","Desemparelhando dispositivo, aguarde..."),
            QCoreApplication.translate("LoggerWidgetText","Sucesso no desemparelhamento"),
            QCoreApplication.translate("LoggerWidgetText","Fim da busca por dispositivos"),
            QCoreApplication.translate("LoggerWidgetText","Procurando por dispositivos, aguarde...")
        ]

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
        self.reloadListButton.clicked.connect(lambda: self.logModel.append_log(self.logger_window_translatable_strings[6]))
        
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
        try:
            if self._connected_device_watcher == False:
                self.deviceContainerFrame.setStyleSheet("""background-color: #1D1B19;""")
            else:
                self.deviceContainerFrame.setStyleSheet("""background-color: #F89E59;""")
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel device_container_style_change error: {e}")

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
        try:
            if self._selected_list_item != None:
                self.pairDeviceButton.setEnabled(True)
            else:
                self.pairDeviceButton.setEnabled(False)
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel pair_button_state_watcher error: {e}")

    @property
    def connected_device_watcher(self):
        return self._connected_device_watcher
    
    @connected_device_watcher.setter
    def connected_device_watcher(self, state):
        self._connected_device_watcher = state
        self.unpair_device_button_watcher()

    def unpair_device_button_watcher(self):
        try:
            if self._connected_device_watcher:
                self.unpairDeviceButton.setEnabled(True)
            else:
                self.unpairDeviceButton.setEnabled(False)
            self.device_container_style_change()
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel unpair_device_button_watcher error: {e}")

    #clears every relevant variable, releses ui and clears list
    def nuke_screen_on_error(self):
        try:
            self.bluetoothHandle.stop_all_processes()
            self.selected_device = [None, None]
            self.deviceListWidget.clear()
            self.selected_list_item = None
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel nuke_screen_on_error - error: {e}")

    #full pair error fallback
    def handle_process_ending_error(self,message):
        try:
            self.logModel.append_log(message)
            logger.error(message)
            self.nuke_screen_on_error()
            self.to_idle.emit()
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel handle_process_ending_error - error: {e}")

    # to garantee button state consistency, both pair and unpair button get called on disable and enable screen,
    def disable_screen(self):
        try:
            self.pairDeviceButton.setEnabled(False)
            self.unpairDeviceButton.setEnabled(False)
            self.reloadListButton.setEnabled(False)
            self.deviceListWidget.setEnabled(False)
            self.sideMenuDisableSignal.emit(False)
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel disable_screen - error: {e}")
        
    def release_screen(self):
        try:
            # for button in self.ui.windowContainer.findChildren(QPushButton):
            #     button.setEnabled(True)
            self.pairDeviceButton.setEnabled(True)
            self.unpairDeviceButton.setEnabled(True)
            self.reloadListButton.setEnabled(True)
            self.deviceListWidget.setEnabled(True)
            self.pair_button_state_watcher()
            self.unpair_device_button_watcher()
            self.sideMenuDisableSignal.emit(True)
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel release_screen - error: {e}")
            
    #adds connected device widget to the layout
    def show_connected_device(self):
        try:
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
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel show_connected_device - error: {e}")

    #clears port addr and mac
    # def clear_serial_info(self):
    #     self.serialHandleClass.clear_serial_info()

    #gets info from the currently selected device from the list and updates self.selected_device
    def device_select_handle(self, index):
        try:
            item = self.sender().item(index.row())
            widget = self.sender().itemWidget(item)
            if widget.isEnabled():
                device_id = widget.deviceDict["id"]
                service_uuid = widget.deviceDict["uuid"]
                self.selected_device[0] = self.bluetoothHandle.hid_device_list[device_id]
                self.selected_device[1] = service_uuid
                self.machine.selected_device = self.selected_device
                self.selected_list_item = index.row()
                self.logModel.append_log(f"{self.logger_window_translatable_strings[0]} {self._selected_list_item+1}")
                logger.debug(f"device_select_handle self.selected_device: {self.selected_device}")
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel device_select_handle - error: {e}")

    #checks for selected devices and starts the full pair
    def pair_selected_device(self):
        try:
            if self.selected_device[0] and self.selected_device[1]:
                self.logModel.append_log(self.logger_window_translatable_strings[1])
                self.machine.full_pair = True
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel pair_selected_device - error: {e}")
            
    #gets device addr            
    def end_full_pair(self,addr = None):
        logger.debug(f"end_full_pair addr:{addr}")
        try:
            self.successful_pair()
        except Exception as e:
            self.handle_process_ending_error(f"Erro ao encontrar dispositivos\nErro: {e}")
            logger.error(f"SharedConnectionManagerModel end_full_pair - error: {e}")

    #will recive the signal from serial handle that indicates if the port was found successfully
    def port_found_signal(self,signal):
        try:
            if signal == True:
                self.successful_pair()
            elif signal == False:
                self.handle_process_ending_error("Erro ao tentar obter porta serial do joystick")
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel port_found_signal - error: {e}")

    def successful_pair(self):
        try:
            self.jsonWriter.write_devices(deviceDict={"mac":self.selected_device[0].address().toString().lower(),"uuid":self.selected_device[1],"name":self.selected_device[0].name()})
            self.show_connected_device()
            item = self.deviceListWidget.takeItem(self._selected_list_item)
            del item
            self.bluetoothHandle.paired_device = self.selected_device[0]
            self.selected_device = [None,None]
            self.selected_list_item = None
            self.logModel.append_log(self.logger_window_translatable_strings[2])
            self.serialBtClass.conn_lost.connect(self.conn_lost_check)
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel successful_pair - error: {e}")
        
    def full_unpair(self):
        self.logModel.append_log(self.logger_window_translatable_strings[3])
        self.machine.full_pair = False
           
    def unpair_finish_handler(self):
        try:
            # self.clear_serial_info()
            self.selected_device = [None,None]
            self.connected_item.deleteLater()
            self.selected_list_item = None
            self.bluetoothHandle.paired_device = None
            self.connected_device_watcher = False
            self.logModel.append_log(self.logger_window_translatable_strings[4])
            self.to_idle.emit()
        except Exception as e:
            logger.error(f"SharedConnectionManagerModel unpair_finish_handler - error: {e}")
        
    #visually updates the list and atributes deviceDict to each item
    def update_list(self):
        try:
            
            self.deviceListWidget.clear()
            
            for i, listed_device_dict in enumerate(self.bluetoothHandle.unified_list):
                if (self.bluetoothHandle.paired_device == None or self.bluetoothHandle.paired_device.address() != listed_device_dict["device"].address()) and listed_device_dict["service"] != None: 

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

            self.logModel.append_log(self.logger_window_translatable_strings[5])
                    
        except IndexError as e:
            logger.error(f"index out of range error")
        except Exception as e:
            logger.error(f"update_list error: {e}")
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
            logger.error(f"SharedConnectionManagerModel cached_device_check - error: {e}")
        
    def state_machine_init(self):
        try:
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

        except Exception as e:
            logger.error(f"SharedConnectionManagerModel state_machine_init - error: {e}")
                        
    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.logger_window_translatable_strings = [
                QCoreApplication.translate("LoggerWidgetText","Dispositivo selecionado:"),
                QCoreApplication.translate("LoggerWidgetText","Emparelhando dispositivo selecionado, aguarde..."),
                QCoreApplication.translate("LoggerWidgetText","Sucesso no emparelhamento"),
                QCoreApplication.translate("LoggerWidgetText","Desemparelhando dispositivo, aguarde..."),
                QCoreApplication.translate("LoggerWidgetText","Sucesso no desemparelhamento"),
                QCoreApplication.translate("LoggerWidgetText","Fim da busca por dispositivos"),
                QCoreApplication.translate("LoggerWidgetText","Procurando por dispositivos, aguarde...")
            ]
        return super().changeEvent(event)
