from PySide6.QtCore import QObject, QByteArray, Signal, QTimer, Qt
from PySide6.QtTest import QSignalSpy
from PySide6.QtWidgets import QWidget

from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm

from shared_ui_modules.ui.model.stacked_widget_screens.calibration_shared_model import SharedCalibrationModel

import pytestqt
import pytest_mock
from unittest.mock import Mock 



class FakeSocket(QObject):
    
    readyRead = Signal()
    
    def __init__(self):
        super().__init__()

        self.data = None

    def readAll(self):
        if self.data:
            return QByteArray(self.data)
    
    def isOpen(self):
        return True

class FakeLogModel(QObject):
    
    def __init__(self):
        super().__init__()

    def append_log(self,message):
        print(message)

class TestCalibrationWidget:
    
    def setup_method(self,method):
        self.fake_log = FakeLogModel()
        self.fake_socket = FakeSocket()
        self.btSerial = SharedBtSerialComm()
        self.btSerial.bt_socket = self.fake_socket
        self.callibration_model = SharedCalibrationModel(logModel=self.fake_log,btSerialhandle=self.btSerial)

    def test_step_0_timeout_success(self,qtbot):
        qtbot.addWidget(self.callibration_model)

        send_serial_message_mock = Mock()
        step_end_mock = Mock()

        self.callibration_model.send_serial_message = send_serial_message_mock
        self.callibration_model.step_end = step_end_mock

        self.callibration_model.serial_messages = ["0","0"]#just for testing
        self.callibration_model.timeout_counter = 9
        
        self.callibration_model.step_0_timeout()

        send_serial_message_mock.assert_called_once()

        self.callibration_model.step_0_timeout()
        
        step_end_mock.assert_called_once()
        
    def test_step_1_timeout_success(self,qtbot):
        qtbot.addWidget(self.callibration_model)

        send_serial_message_mock = Mock()
        step_end_mock = Mock()

        self.callibration_model.send_serial_message = send_serial_message_mock
        self.callibration_model.step_end = step_end_mock

        self.callibration_model.serial_messages = ["0","0"]#just for testing
        self.callibration_model.timeout_counter = 9
        
        self.callibration_model.step_0_timeout()

        send_serial_message_mock.assert_called_once()

        self.callibration_model.step_0_timeout()
        
        step_end_mock.assert_called_once()

    def test_step_end(self,qtbot):
        qtbot.addWidget(self.callibration_model)
        
        present_result_mock = Mock()
        update_instructions_mock = Mock()
        
        self.callibration_model.update_instruction_ui = update_instructions_mock
        self.callibration_model.present_results = present_result_mock
        self.callibration_model.calibration_step = 0

        self.callibration_model.step_end()

        assert self.callibration_model.timeout_counter == 0
        update_instructions_mock.assert_called_once()

        self.callibration_model.calibration_step = 1

        self.callibration_model.step_end()

        assert self.callibration_model.timeout_counter == 0
        present_result_mock.assert_called_once()

