from shared_ui_modules.modules.log_class import logger

from PySide6.QtBluetooth import QBluetoothServiceInfo, QBluetoothSocket, QBluetoothUuid, QBluetoothAddress
from PySide6.QtCore import QObject, QTimer, QIODevice, Signal

import re

baud_rate = 600

class BtSerialComm(QObject):

    port_finish = Signal()
    port_error = Signal()
    mesReceivedSignal = Signal(object)
    conn_lost = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)

        #module setup
        self.bt_socket = None
        self.timer = QTimer()

        #variable setup
        self.pause_var = False
        self.message_buffer = ""
        self.use_data_buffer = ""
        self.use_data_regex = r"\*I\d{12}"
        
        self.timer.timeout.connect(self.handle_timeout)

    def alter_port_state(self,state = True):
        if state == False:
            self.bt_socket.close()
        else:
            self.bt_socket.open()

    def socket_none_check(self):
        if not self.bt_socket:
            logger.debug(f"SharedBtSerialHandle none socket")
            self.port_error.emit()
            return True
        else:
            return False

 # if port not open
    def open_port(self):
        if self.socket_none_check():
            return
        try:
            if not self.bt_socket.isOpen():
                if not self.bt_socket.open(QIODevice.ReadWrite):
                    logger.error(f"Erro ao abrir porta serial: {self.bt_socket.errorString()}")
        except AttributeError as e:
            logger.debug(f"open_port error: {e}")
            self.port_error.emit()
            
    #on sucessfull read stop reading for 1 sec, deals with multiple messages of same value
    def start_timer(self):
        self.timer.start(1000)
        self.pause_var = True
        
    def handle_timeout(self):
        self.pause_var = False
        self.bt_socket.readAll()#!find a way to clear the bt_socket port

    def swap_message_listner(self,op = 0):
        if self.socket_none_check():
            return
        self.bt_socket.readyRead.disconnect()
        if op == 0:#default
            self.bt_socket.readyRead.connect(self.recieve_message)
        elif op == 1:#use_data_collector
            self.bt_socket.readyRead.connect(self.recieve_use_data_message)

    #logs error on serial
    def handle_serial_error(self,err):
        logger.debug(f"socket_error_handle error:{err}")
        self.port_error.emit()

    #gets message from model class and writes it
    def send_message(self, message):
        if self.socket_none_check():
            return
        try:
            logger.debug(f"send_message message:{message}")
            encodedMessage = message.encode('utf-8')
            self.bt_socket.write(encodedMessage)
        except AttributeError as e:
            logger.debug(f"send_message error: {e}")
            self.port_error.emit()

    #gets message, decodes, sends signal
    def recieve_message(self):
        if self.socket_none_check():
            return
        try:
            message_substrings = []#mesages to be sent
            data = self.bt_socket.readAll()#these messages can be recieved in any way at any time, so it can be split or concateneted
            dataStr = data.toStdString()
            self.message_buffer += dataStr
            print(f"recive_message:{self.message_buffer}")
            while "N" in self.message_buffer or "A" in self.message_buffer:
                last_index = 0
                for i, c in enumerate(self.message_buffer):#get the substring up to the limiter
                    if c == "A" or c == "N":
                        message_substrings.append(self.message_buffer[:i+1])
                        last_index = i
                        break
                self.message_buffer = self.message_buffer[last_index+1:]
            for m in message_substrings:
                self.mesReceivedSignal.emit(m)
                logger.debug(f"Mensagem recebida: {m}")
        except AttributeError as e:
            logger.debug(f"recieve_message error: {e}")
            self.port_error.emit()

#receives sensor readings
    def recieve_use_data_message(self):
        if self.socket_none_check():
            return
        try:
            if self.pause_var != True:
                messages = []
                data = self.bt_socket.readAll()
                dataStr = data.toStdString()
                self.use_data_buffer += dataStr
                matches = list(re.finditer(self.use_data_regex,self.use_data_buffer))
                print(f"recieve_use_data_message self.use_data_buffer:{self.use_data_buffer}\ndataStr:{dataStr}\nmatches:{matches}")
                if matches:
                    last_match = matches[-1]
                    start, end = last_match.span()
                    self.use_data_buffer = self.message_buffer[end+1:]
                    self.start_timer()
                for m in matches:
                    messages.append(m.group())
                    logger.debug(f"Mensagem recebida: {m.group()}")
                if messages:
                    self.mesReceivedSignal.emit(messages)
        except AttributeError as e:
            logger.debug(f"recieve_use_data_message error: {e}")
            self.port_error.emit()

    def create_service_socket(self, addr = None, uuid = None):
        try:
            self.clear_socket()
            logger.debug(f"create_service_socket service:{addr,uuid}")

            self.bt_socket = QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)

            self.bt_socket.readyRead.connect(self.recieve_message)
            self.bt_socket.errorOccurred.connect(self.handle_serial_error)
            self.bt_socket.connected.connect(self.socket_connect_handle)
            self.bt_socket.destroyed.connect(self.socket_deleted)
            self.bt_socket.stateChanged.connect(self.socket_state_change)
            
            if addr and uuid:
                logger.debug(f"create_service_socket service true")
                self.bt_socket.connectToService(addr,uuid)
        except:
            self.port_error.emit()

    def clear_socket(self):
        if self.bt_socket:
            self.bt_socket.disconnectFromService()
            self.bt_socket.connected.disconnect(self.socket_connect_handle)
            self.bt_socket.errorOccurred.disconnect(self.handle_serial_error)
            self.bt_socket.readyRead.disconnect(self.recieve_message)
            self.bt_socket.stateChanged.disconnect(self.socket_state_change)
            self.bt_socket.deleteLater()

    def socket_connect_handle(self):
        logger.debug(f"socket_connect_handle")
        self.open_port()
        self.send_message('0')
        self.port_finish.emit()

    def socket_deleted(self):
        self.bt_socket = None
        
    #check if socket state is UnconnectedState
    #this has to come after a RemoteHostClosedError or has to happen while a connected device object exist to be a problem
    def socket_state_change(self,state):
        logger.debug(f"SharedBTSerial socket_state_change state: {state}")
        if state == QBluetoothSocket.SocketState.UnconnectedState:
            self.conn_lost.emit()