from PySide6.QtCore import QObject, QByteArray, Signal, QTimer, Qt
from PySide6.QtTest import QSignalSpy

from PySide6.QtBluetooth import (QBluetoothLocalDevice, QBluetoothServiceDiscoveryAgent, QBluetoothServiceInfo,
                                 QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QLowEnergyController, QBluetoothSocket)

from shared_ui_modules.modules.bluetooth_comunication import BluetoothCommClass
from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm
from shared_ui_modules.ui.model.stacked_widget_screens.connection_manager_model import SharedConnectionManagerModel

from unittest.mock import Mock 
import pytestqt

class FakeLogModel(QObject):
    
    def __init__(self):
        super().__init__()

    def append_log(self,message):
        print(message)

class FakeBluetoohHandle(QObject):

    hid_finish = Signal(str)
    spp_finish = Signal(str)
    le_finish = Signal(object)

    hid_error = Signal()
    spp_error = Signal()
    local_error = Signal()
    le_error = Signal()

    def __init__(self):
        super().__init__()

        self.spp_service_list = []
        self.hid_device_list = []
        self.powered_device_list = []
        self.le_controller_list = []
        self.unified_list = []
        self.paired_device = []

    def hid_device_discovery(self):
        print(f"FakeBluetoohHandle hid_device_discoverys")
        QTimer.singleShot(
            1000,
            lambda: self.hid_finish.emit("hid")
        )

    def spp_service_discovery(self):
        print(f"FakeBluetoohHandle spp_service_discovery")
        QTimer.singleShot(
            2000,
            lambda: self.spp_finish.emit("spp")
        )

    def hid_device_unpair(self,device):
        print(f"FakeBluetoohHandle hid_device_unpair")
        QTimer.singleShot(
            1000,
            lambda: self.hid_finish.emit("hid")
        )

    def unpair_device(self,service):
        print(f"FakeBluetoohHandle unpair_device")
        QTimer.singleShot(
            1500,
            lambda: self.spp_finish.emit("spp")
        )

    def low_energy_check(self,device: QBluetoothDeviceInfo):
        controller = QLowEnergyController.createCentral(device)
        self.le_controller_list.append(controller)
        QTimer.singleShot(
            500,
            lambda: self.le_finish.emit(device.address())
        )

    def check_device_connection(self,device):
        self.hid_finish.emit("hid")
    
class TestConnectionManager:
    
    def setup_method(self,method):
        self.bt_serial_class = SharedBtSerialComm()
        
    def test_update_list_success(self,qtbot,monkeypatch):
        conn_manager = SharedConnectionManagerModel(logModel=None,serialBtClass=self.bt_serial_class)

        #simulation
            #Finds a service and turned off device 
        device = QBluetoothDeviceInfo()
        service = QBluetoothServiceInfo()
        service.setDevice(device)

        conn_manager.bluetoothHandle.unified_list = [{
            "device":device,
            "turned_on":False,
            "service":service
        }]

        conn_manager.update_list()

        turned_off_device_item = conn_manager.deviceListWidget.itemWidget(conn_manager.deviceListWidget.item(0))

        assert conn_manager.deviceListWidget.count() == 1  
        assert turned_off_device_item.isEnabled() == False

        conn_manager.bluetoothHandle.unified_list = [{
            "device":device,
            "turned_on":False,
            "service":service
        },
        {
            "device":device,
            "turned_on":True,
            "service":service
        },
        {
            "device":device,
            "turned_on":True,
            "service":service
        },
        {
            "device":device,
            "turned_on":False,
            "service":service
        },
        {
            "device":device,
            "turned_on":False,
            "service":None
        },
        None,                                          
        {
            "device":None,
            "turned_on":None,
            "service":service
        }
        ]

        conn_manager.update_list()
        
        turned_off_device_item = [conn_manager.deviceListWidget.itemWidget(conn_manager.deviceListWidget.item(0)),conn_manager.deviceListWidget.itemWidget(conn_manager.deviceListWidget.item(3))]
        turned_on_device_item = [conn_manager.deviceListWidget.itemWidget(conn_manager.deviceListWidget.item(1)),conn_manager.deviceListWidget.itemWidget(conn_manager.deviceListWidget.item(2))]

        assert conn_manager.deviceListWidget.count() == 4
        assert turned_off_device_item[0].isEnabled() == turned_off_device_item[0].isEnabled() == False
        assert turned_on_device_item[0].isEnabled() == turned_on_device_item[0].isEnabled() == True

    def test_show_connceted_device_success(self,qtbot,monkeypatch):
        device = QBluetoothDeviceInfo()

        conn_manager = SharedConnectionManagerModel(logModel=None,serialBtClass=self.bt_serial_class)

        conn_manager.selected_device[0] = device

        conn_manager.show_connected_device()
        
        connected_device_widget = conn_manager.connected_item
        
        assert conn_manager.connected_device_watcher == True
        assert connected_device_widget.deviceNameLabel.text() == device.name()
        assert connected_device_widget.macLabel.text() == device.address().toString()
        
    def test_release_screen_success(self,qtbot,monkeypatch):
        conn_manager = SharedConnectionManagerModel(logModel=None,serialBtClass=self.bt_serial_class)
        pair_button_state_watcher_mock = Mock()
        unpair_device_button_watcher_mock = Mock()

        sigSpy_sideMenuDiableSignal = QSignalSpy(conn_manager.sideMenuDisableSignal)

        monkeypatch.setattr(
            conn_manager,
            "pair_button_state_watcher",
            pair_button_state_watcher_mock
        )
        monkeypatch.setattr(
            conn_manager,
            "unpair_device_button_watcher",
            unpair_device_button_watcher_mock
        )
        
        conn_manager.release_screen()

        assert conn_manager.pairDeviceButton.isEnabled() == True
        assert conn_manager.unpairDeviceButton.isEnabled() == True
        assert conn_manager.reloadListButton.isEnabled() == True
        assert conn_manager.deviceListWidget.isEnabled() == True
        assert sigSpy_sideMenuDiableSignal.count() == 1
        unpair_device_button_watcher_mock.assert_called_once()
        pair_button_state_watcher_mock.assert_called_once()
        
    def test_disable_screen_success(self,qtbot,monkeypatch):        
        conn_manager = SharedConnectionManagerModel(logModel=None,serialBtClass=self.bt_serial_class)
        sigSpy_sideMenuDiableSignal = QSignalSpy(conn_manager.sideMenuDisableSignal)

        
        conn_manager.disable_screen()

        assert conn_manager.pairDeviceButton.isEnabled() == False
        assert conn_manager.unpairDeviceButton.isEnabled() == False
        assert conn_manager.reloadListButton.isEnabled() == False
        assert conn_manager.deviceListWidget.isEnabled() == False
        assert sigSpy_sideMenuDiableSignal.count() == 1

    def test_nuke_screen_on_error_success(self,qtbot,monkeypatch):
        conn_manager = SharedConnectionManagerModel(logModel=None,serialBtClass=self.bt_serial_class)
        
        conn_manager.nuke_screen_on_error()

        assert conn_manager.selected_device == [None,None]
        assert conn_manager.deviceListWidget.count() == 0
        assert conn_manager.selected_list_item == None

    def test_reload_list_button_success(self,qtbot,monkeypatch):
        fake_log_model = FakeLogModel()        
        fake_bt_handle = FakeBluetoohHandle()

        conn_manager = SharedConnectionManagerModel(logModel=fake_log_model,serialBtClass=self.bt_serial_class)
        qtbot.wait(2000)

        conn_manager.search_state.btHandle = fake_bt_handle

        sigSpy_search_end = QSignalSpy(conn_manager.search_state.search_end)

        qtbot.addWidget(conn_manager)

        conn_manager.reloadListButton.click()

        assert conn_manager.pairDeviceButton.isEnabled() == False
        assert conn_manager.unpairDeviceButton.isEnabled() == False
        assert conn_manager.reloadListButton.isEnabled() == False
        assert conn_manager.deviceListWidget.isEnabled() == False
        assert conn_manager.search_state.active() == True

        qtbot.waitUntil(
            lambda: sigSpy_search_end.count() > 0,
            timeout = 5000
        )

        assert sigSpy_search_end.count() == 1

        device = QBluetoothDeviceInfo()
        service = QBluetoothServiceInfo()
        service.setDevice(device)
        
        conn_manager.search_state.btHandle.spp_service_list = [service] 
        conn_manager.search_state.btHandle.hid_device_list = [device]

        cached_check_mock = Mock()
        
        def fake_clear_le_controller(controller):
            conn_manager.search_state.btHandle.unified_list = conn_manager.search_state.unify_list()
            conn_manager.bluetoothHandle.unified_list = conn_manager.search_state.btHandle.unified_list
            conn_manager.search_state.service_null_check()

        monkeypatch.setattr(
            conn_manager.search_state,
            "clear_le_controller",
            lambda controller: fake_clear_le_controller(controller)
        )

        monkeypatch.setattr(
            conn_manager.search_state,
            "cached_check",
            cached_check_mock
        )
        
        conn_manager.reloadListButton.click()

        assert conn_manager.pairDeviceButton.isEnabled() == False
        assert conn_manager.unpairDeviceButton.isEnabled() == False
        assert conn_manager.reloadListButton.isEnabled() == False
        assert conn_manager.deviceListWidget.isEnabled() == False
        assert conn_manager.search_state.active() == True

        qtbot.waitUntil(
            lambda: sigSpy_search_end.count() > 1,
            timeout = 5000
        )

        assert sigSpy_search_end.count() > 1
        assert len(conn_manager.search_state.btHandle.unified_list) == 1
        assert conn_manager.search_state.btHandle.unified_list ==[{
            "device":device,
            "turned_on": False,
            "service":service.serviceUuid().toString()
        }]

        assert conn_manager.deviceListWidget.count() == 1

    def test_disconnect_case_0_success(self,qtbot,monkeypatch):
        device = QBluetoothDeviceInfo()
        service = QBluetoothServiceInfo()
        service.setDevice(device)

        fake_bt_handle = FakeBluetoohHandle()
        fake_log_class = FakeLogModel()

        conn_manager = SharedConnectionManagerModel(logModel=fake_log_class,serialBtClass=self.bt_serial_class)
        qtbot.wait(1000)
        
        qtbot.addWidget(conn_manager)

        disc_state = conn_manager.disconnect_state
        disc_state.btHandle = fake_bt_handle
        
        conn_manager.selected_device = [device,service]
        conn_manager.machine.selected_device = [None]

        conn_manager.show_connected_device()
        disc_state.btHandle.paired_device = device

        sigSpy_disc_finish = QSignalSpy(disc_state.disc_finish)

        # conn_check_mock = Mock()

        # monkeypatch.setattr(
        #     disc_state,
        #     "conn_check",
        #     conn_check_mock
        # )

        conn_manager.unpairDeviceButton.click()
        
        assert conn_manager.connected_device_watcher == True
        assert disc_state.machine.full_pair == False
        
        # qtbot.waitUntil(
        #     lambda: conn_check_mock.call_count > 0,
        #     timeout = 5000
        # )
        
        # conn_check_mock.assert_called_once()

        qtbot.waitUntil(
            lambda: sigSpy_disc_finish.count() > 0,
            timeout = 5000
        )

        assert sigSpy_disc_finish.count() == 1

    #!needs a turned on controller to work 
    def test_find_device_connect_send_message_disconnect_success(self,qtbot,monkeypatch):
        #setup
        fake_log_model = FakeLogModel()        

        conn_manager = SharedConnectionManagerModel(logModel=fake_log_model,serialBtClass=self.bt_serial_class)
        qtbot.wait(500)

        sigSpy_search_end = QSignalSpy(conn_manager.search_state.search_end)

        #find the device 
        conn_manager.reloadListButton.click()

        qtbot.waitUntil(
            lambda: conn_manager.deviceListWidget.count() > 0,
            timeout = 1000000
        )

        assert conn_manager.deviceListWidget.count() == 1

        #get item position on list
        item_pos = conn_manager.deviceListWidget.visualItemRect(conn_manager.deviceListWidget.item(0))

        #select item on list
        qtbot.mouseClick(
            conn_manager.deviceListWidget.viewport(),
            Qt.LeftButton,
            pos = item_pos.center()
        )

        #pair the device
        conn_manager.pairDeviceButton.click()

        sigSpy_pair_success = QSignalSpy(conn_manager.find_port_state.pair_success)
        
        json_writer_mock = Mock()
        json_writer_mock.write_devices = Mock()

        conn_manager.jsonWriter = json_writer_mock
        
        qtbot.waitUntil(
            lambda:  sigSpy_pair_success.count() > 0,
            timeout = 100000
        )

        assert conn_manager._connected_device_watcher == True
        assert conn_manager.connected_item != None
        
        #try to send a serial mesage       
        sigSpy_mes_recieved = QSignalSpy(conn_manager.serialBtClass.mesReceivedSignal)

        conn_manager.serialBtClass.send_message("*T0")
        
        qtbot.waitUntil(
            lambda:sigSpy_mes_recieved.count() > 0 
        )

        assert sigSpy_mes_recieved.count() > 0
        assert sigSpy_mes_recieved.at(0)[0] == "A"

        #disconnect the device
        sigSpy_conn_finish = QSignalSpy(conn_manager.disconnect_state.disc_finish)

        assert conn_manager.unpairDeviceButton.isEnabled() == True
        
        conn_manager.unpairDeviceButton.click()

        qtbot.waitUntil(
            lambda: sigSpy_conn_finish.count() > 0,
            timeout = 100000
        )

        assert conn_manager._connected_device_watcher == False