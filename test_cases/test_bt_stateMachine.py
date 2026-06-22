from PySide6.QtCore import QObject, QByteArray, Signal
from PySide6.QtTest import QSignalSpy
from PySide6.QtStateMachine import QStateMachine

from PySide6.QtBluetooth import (QBluetoothLocalDevice, QBluetoothServiceDiscoveryAgent, QBluetoothServiceInfo,
                                 QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QLowEnergyController, QBluetoothSocket)

from shared_ui_modules.modules.bluetooth_comunication import BluetoothCommClass
from shared_ui_modules.modules.connection_manager_state_machine import IdleState, ErrorState, FindPortState, ConnectionState, DeviceSearchState, DisconnectionState
from shared_ui_modules.ui.model.stacked_widget_screens.connection_manager_model import SharedConnectionManagerModel

from unittest.mock import Mock 
import pytestqt

class TesteBtStateMachine:
    
    def setup_method(self,method):
        self.bt_comm_class = BluetoothCommClass()
        # self.conn_manager = SharedConnectionManagerModel(logModel=None,serialBtClass=self.bt_comm_class)

    def test_disconneciton_case_evaluation_success(self,qtbot,monkeypatch):
        machine = QStateMachine()
        machine.selected_device = [None]
        
        bt = Mock()
        bt.paired_device = Mock()
        
        state = DisconnectionState(machine=machine,bluetoothHandle=bt,btSerialHandle=None,functions=None)

        res = state.case_evaluation()

        assert res == 0

        state.machine.selected_device = [Mock()]
        state.btHandle.paired_device = None
        res = state.case_evaluation()

        assert res == 1

        state.machine.selected_device = [Mock()]
        state.btHandle.paired_device = Mock()
        res = state.case_evaluation()

        assert res == 2

    def test_disconnection_async_check_suc(self,qtbot,monkeypatch):
        machine = QStateMachine()
        machine.selected_device = [None]
        machine.full_pair = True
        machine.spp_watcher = False
        machine.hid_watcher = False
        
        bt = Mock()
        bt.paired_device = Mock()
        
        state = DisconnectionState(machine=machine,bluetoothHandle=bt,btSerialHandle=None,functions=None)

        state.async_check("hid")
        res = state.async_check("spp")

        assert res == "conn_start"

        state.machine.full_pair = False

        state.async_check("spp")
        res = state.async_check("hid")

        assert res == "disc_finish"

    def test_disconnection_handle_finish_suc(self,qtbot,monkeypatch):
        machine = QStateMachine()
        machine.selected_device = [None]
        machine.full_pair = False
        machine.spp_watcher = False
        machine.hid_watcher = False
        
        bt = Mock()
        bt.paired_device = Mock()
        
        state = DisconnectionState(machine=machine,bluetoothHandle=bt,btSerialHandle=None,functions=None)
        conn_check_mock = Mock()
        monkeypatch.setattr(
            state,
            "conn_check",
            conn_check_mock
        )
        sigSpy_conn_start = QSignalSpy(state.conn_start)
        
        state.handle_finish("hid")
        state.handle_finish("spp")

        conn_check_mock.assert_called_once()

        state.machine.full_pair = True
        state.handle_finish("hid")
        state.handle_finish("spp")

        assert sigSpy_conn_start.count() == 1

    def test_disconnect_on_exit_sucess(self,qtbot,monkeypatch):
        machine = QStateMachine()
        machine.selected_device = [None]
        machine.full_pair = False
        machine.spp_watcher = False
        machine.hid_watcher = False
        
        bt = Mock()
        bt.paired_device = Mock()
        
        state = DisconnectionState(machine=machine,bluetoothHandle=bt,btSerialHandle=None,functions=None)

        state.onExit(None)

        assert state.machine.full_pair == None
        assert state.sp_case == None
        assert state.spp_counter == 0
        assert state.hid_counter == 0
    
    def test_connection_async_check_success(self,qtbot,monkeypatch):
        state = ConnectionState(machine=None,bluetoothHandle=None,functions=None)

        res = state.async_check("hid")
        
        assert res == "conn_finish"

        res = state.async_check("")
        
        assert res == None
        
    def test_connection_handle_finish_success(self,qtbot,monkeypatch):
        machine = QStateMachine()
        machine.selected_device = [QBluetoothDeviceInfo()]
        state = ConnectionState(machine=machine,bluetoothHandle=None,functions=None)

        sigSpy_conn_finish = QSignalSpy(state.conn_finish)

        state.handle_finish("hid")

        assert sigSpy_conn_finish.count() == 1

        #reinstance sigSpy since i cant clear it 
        sigSpy_conn_finish = QSignalSpy(state.conn_finish)

        state.handle_finish("")

        assert sigSpy_conn_finish.count() == 0

    def test_search_async_check_success(self,qtbot,monkeypatch):
        machine = QStateMachine()
        machine.search = True
        machine.hid_watcher = False
        machine.spp_watcher = False
        
        state = DeviceSearchState(machine=machine,bluetoothHandle=None,functions=None,logModel=None)

        state.async_check("hid")
        res = state.async_check("spp")

        assert res == "search_end"

        state.machine.search = None

        state.async_check("hid")
        res = state.async_check("spp")

        assert res == None

        state.machine.search = True
        
        state.async_check("hid")
        res = state.async_check("hid")

        assert res == None
        
        state.async_check("spp")
        res = state.async_check("spp")

        assert res == None

    def test_search_handle_finish_sucess(self,qtbot,monkeypatch):
        machine = QStateMachine()
        machine.search = True
        machine.hid_watcher = False
        machine.spp_watcher = False
        
        state = DeviceSearchState(machine=machine,bluetoothHandle=None,functions=None,logModel=None)
        device_power_check_mock = Mock()
        monkeypatch.setattr(
            state,
            "device_power_check",
            device_power_check_mock
        )

        state.handle_finish("spp")
        state.handle_finish("hid")

        device_power_check_mock.assert_called_once()

        state.handle_finish("hid")
        state.handle_finish("hid")

        assert device_power_check_mock.call_count == 1

        state.handle_finish("spp")

        assert device_power_check_mock.call_count == 2

    def test_search_handle_power_finish_success(self,qtbot,monkeypatch):
        btHandle = Mock()
        btHandle.powered_device_list = []
        btHandle.le_controller_list = [True,True,True,True,True]

        state = DeviceSearchState(machine=None,bluetoothHandle=btHandle,functions=None,logModel=None)

        clear_le_controller_mock = Mock()

        monkeypatch.setattr(
            state,
            "clear_le_controller",
            clear_le_controller_mock
        )
        
        state.device_counter = 5

        for i in range(0,5):
            state.handle_power_finish(True)

        assert state.device_counter == 0
        clear_le_controller_mock.assert_called_with(True)
        assert clear_le_controller_mock.call_count == 5

        state.device_counter = 5

        for i in range(0,5):
            state.handle_power_finish(False)

        assert state.device_counter == 0
        clear_le_controller_mock.assert_called_with(True)
        assert clear_le_controller_mock.call_count == 10

        state.device_counter = 5

        state.handle_power_finish(False)
        state.handle_power_finish(False)
        state.handle_power_finish(False)
        state.handle_power_finish(True)
        state.handle_power_finish(True)

        assert state.device_counter == 0
        clear_le_controller_mock.assert_called_with(True)
        assert clear_le_controller_mock.call_count == 15
        
    def test_search_fallback_return_result_success(self,qtbot,monkeypatch):
        
        state = DeviceSearchState(machine=None,bluetoothHandle=None,functions=None,logModel=None)

        sigSpy_search_end = QSignalSpy(state.search_end)

        state.pending_callbacks = {"0":{"service":None},"1":{"service":None}}

        state.fallback_return_result(message={"mac":"0","uuid":"0"})
        
        assert sigSpy_search_end.count() == 0

        state.fallback_return_result(message={"mac":"0","uuid":"0"})

        assert sigSpy_search_end.count() == 0

        state.fallback_return_result(message=None)
        
        assert sigSpy_search_end.count() == 0

        state.fallback_return_result(message={"mac":"1","uuid":123})

        assert sigSpy_search_end.count() == 1

    def test_search_service_null_check_success(self,qtbot,monkeypatch):
        bt = Mock()
        bt.unified_list = [{"device": QBluetoothDeviceInfo(),"turned_on": False,"service": None},
                            {"device": QBluetoothDeviceInfo(),"turned_on": True,"service": None},
                            {"device": QBluetoothDeviceInfo(),"turned_on": True,"service": True}]

        state = DeviceSearchState(machine=None,bluetoothHandle=bt,functions=None,logModel=None)

        cached_check_mock = Mock()
        spp_fallback_mock = Mock()
        
        cached_check_mock.return_value = None

        monkeypatch.setattr(
            state,
            "cached_check",
            cached_check_mock
        )
        monkeypatch.setattr(
            state,
            "spp_fallback",
            spp_fallback_mock
        )

        sigSpy_search_end = QSignalSpy(state.search_end)

        state.service_null_check()

        cached_check_mock.assert_called_once()

        assert sigSpy_search_end.count() == 0

        state.btHandle.unified_list = [{"device": QBluetoothDeviceInfo(),"turned_on": True,"service": None}]

        state.cached_check.return_value = True

        state.service_null_check()
        
        assert sigSpy_search_end.count() == 1

    def test_search_unify_list_success(self,qtbot,monkeypatch):
        #simulation
            #finds one unpowered device with service
            #appends on list
        device = QBluetoothDeviceInfo()
        service = QBluetoothServiceInfo()
        le = QLowEnergyController.createCentral(device)
        service.setDevice(device)
        
        bt = Mock()
        bt.spp_service_list = [
            service
        ]
        bt.powered_device_list = []
        bt.hid_device_list = [
            device
        ]

        state = DeviceSearchState(machine=None,bluetoothHandle=bt,functions=None,logModel=None)

        res = state.unify_list()
        
        assert res == [{
            "device":device,
            "turned_on": False,
            "service": service.serviceUuid().toString()
        }]

        #simulation
            #finds nothing
        state.btHandle.powered_device_list = []
        state.btHandle.hid_device_list = []
        state.btHandle.spp_service_list = []

        res = state.unify_list()

        assert res == []
        
        #simulation
            #finds hid device and nothing else
        state.btHandle.hid_device_list = [device]

        res = state.unify_list()

        assert res == [{
            "device":device,
            "turned_on":False,
            "service":None
        }]
        
    def test_find_port_on_socket_success(self,qtbot,monkeypatch):
        machine = QStateMachine()
        machine.addr = "True"

        state = FindPortState(machine= machine, bluetoothHandle=None, btSerialHandle=None, functions=None)

        sigSpy_pair_success = QSignalSpy(state.pair_success)

        state.on_socket_sucess()

        assert sigSpy_pair_success.count() == 1