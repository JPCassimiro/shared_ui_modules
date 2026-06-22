from PySide6.QtCore import QObject, QByteArray, Signal
from PySide6.QtTest import QSignalSpy

from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm

import pytest
import pytestqt

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

class TestSerial:
    
    def setup_method(self, method):
        
        self.bt_class = SharedBtSerialComm()
        self.fake_socket = FakeSocket()
        self.bt_class.bt_socket = self.fake_socket
        self.bt_class.use_data_regex = r"\*I\d{12}"

    def test_read_all_success(self,qtbot):
        
        mesRecieved_sig_spy = self.reasing_data(b"123N321A")
        self.bt_class.recieve_message()
                
        assert mesRecieved_sig_spy.count() == 2 #success case
        assert mesRecieved_sig_spy.at(0)[0] == "123N" #success case
        assert mesRecieved_sig_spy.at(1)[0] == "321A" #success case

        mesRecieved_sig_spy = self.reasing_data(b"NNNNNNNNNNNNN")
        self.bt_class.recieve_message()
        
        assert mesRecieved_sig_spy.count() == 13 #success case
        
        mesRecieved_sig_spy = self.reasing_data(b"1234567890,.;~]<>:^}{```+_*+-''!@#$%|?&*()[-=zxcvbmsdfghjklqwertyuiop")
        self.bt_class.recieve_message()
        self.bt_class.recieve_message()

        assert mesRecieved_sig_spy.count() == 0 #success case
        
    def test_read_all_fail(self,qtbot):
        
        mesRecieved_sig_spy = self.reasing_data(b"123A123N")
        self.bt_class.recieve_message()
                
        assert mesRecieved_sig_spy.count() == 0 #fail case

    #!connet the readReady signal to the correct funtion and disconnect it in the end of the test
    def test_ready_read_buffer_success(self,qtbot):
        self.bt_class.bt_socket.readyRead.connect(self.bt_class.recieve_message)
        mesRecieved_sig_spy = self.reasing_data(b"000A100A200A300A") 
        self.fake_socket.readyRead.emit()

        assert mesRecieved_sig_spy.count() == 4 #success case
        assert mesRecieved_sig_spy.at(0)[0] == "000A" #success case
        assert mesRecieved_sig_spy.at(1)[0] == "100A" #success case
        assert mesRecieved_sig_spy.at(2)[0] == "200A" #success case
        assert mesRecieved_sig_spy.at(3)[0] == "300A" #success case
        
        self.fake_socket.data = b"00"
        self.fake_socket.readyRead.emit()

        assert self.bt_class.message_buffer == "00" #success case

        mesRecieved_sig_spy = self.reasing_data(b"0A")
        self.fake_socket.readyRead.emit()

        assert mesRecieved_sig_spy.count() == 1 #success case
        assert mesRecieved_sig_spy.at(0)[0] == "000A" #success case
        self.bt_class.bt_socket.readyRead.disconnect(self.bt_class.recieve_message)

    def test_use_data_collection_success(self,qtbot):
        mesRecieved_sig_spy = self.reasing_data(b"*I000010000210")
        self.bt_class.recieve_use_data_message()
        
        assert mesRecieved_sig_spy.count() == 1 #success case
        assert mesRecieved_sig_spy.at(0)[0][0] == "*I000010000210" #success case

    def test_use_data_collection_fail(self,qtbot):
        mesRecieved_sig_spy = self.reasing_data(b"*I000010000210")
        self.bt_class.recieve_use_data_message()
        
        assert mesRecieved_sig_spy.count() == 0 #fail case

    def test_use_data_collection_ready_read_buffer_success(self,qtbot):
        self.bt_class.bt_socket.readyRead.connect(self.bt_class.recieve_use_data_message)

        self.fake_socket.data = "*I"
        self.fake_socket.readyRead.emit()
        self.fake_socket.data = "00"
        self.fake_socket.readyRead.emit()

        assert self.bt_class.use_data_buffer == "*I00"

        self.fake_socket.data = "0210"
        self.fake_socket.readyRead.emit()

        assert self.bt_class.use_data_buffer == "*I000210"

        mesRecieved_sig_spy = self.reasing_data(None)

        self.fake_socket.data = "002100"
        self.fake_socket.readyRead.emit()

        assert mesRecieved_sig_spy.count() == 1
        assert mesRecieved_sig_spy.at(0)[0][0] == "*I000210002100"

        self.bt_class.bt_socket.readyRead.disconnect(self.bt_class.recieve_use_data_message)

    def reasing_data(self,data):
        mesRecieved_sig_spy = QSignalSpy(self.bt_class.mesReceivedSignal)
        self.fake_socket.data = data
        return mesRecieved_sig_spy