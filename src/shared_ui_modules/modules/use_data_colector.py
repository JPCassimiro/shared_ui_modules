from PySide6.QtCore import QObject

from shared_ui_modules.modules.log_class import logger

import time

class SharedDataCollectorClass(QObject):
    def __init__(self, dbHandleClass, btSerialHandle, logModel):
        super().__init__()
        
        self.logModel = logModel
        self.dbHandleClass = dbHandleClass
        self.btSerialHandle = btSerialHandle

        self.message_buffer_reset = None

    def get_message_buffer(self):
        return
    
    def initilize_module(self):
        self.message_buffer_reset = self.get_message_buffer()
        
    #value watcher setup
    #when atributed will check value
    #true = start
    @property
    def start_watch(self):
        return self._start_watch
    
    @start_watch.setter
    def start_watch(self,val):
        self._start_watch = val
        self.start_checker()

    def start_checker(self):
        try:
            if self._start_watch != False:
                if self.btSerialHandle.socket_none_check():
                    raise Exception
                    return
                self.start_data_collection(2500)
                self.send_serial_message("*L1")
                time.sleep(0.5)#attemps to garantee that the response from L1 will be handled on the regular message listner
                self.btSerialHandle.swap_message_listner(1)
                # self.serialHandleClass.swap_message_listner(1)
                self.btSerialHandle.mesReceivedSignal.connect(self.message_received_handler)
                self.btSerialHandle.port_error.connect(self.serial_error_handler)
                # self.serialHandleClass.mesReceivedSignal.connect(self.message_received_handler)
            else:
                self.timer.stop()
                if self.btSerialHandle.socket_none_check():
                    self.timeout_handle()
                    return
                self.btSerialHandle.swap_message_listner(0)
                # self.serialHandleClass.swap_message_listner(0)
                self.btSerialHandle.mesReceivedSignal.disconnect(self.message_received_handler)
                self.btSerialHandle.port_error.disconnect(self.serial_error_handler)
                # self.serialHandleClass.mesReceivedSignal.disconnect(self.message_received_handler)
                self.timeout_handle()
                self.send_serial_message("*L0")
        except Exception as e:
            logger.error(f"Erro ao alterar o processo de coleta: {e}")
            self.message_buffer = self.message_buffer_reset
            self.errorOcurred.emit(True)

    def start_data_collection(self,ms):
        self.timer.start(ms)

    def insert_data(self,q,data):
        res = self.dbHandleClass.execute_multiple_queries(q,data)
        if res:
            logger.debug(f"estatisticas de uso inseridos na tabela: {res[0][0]}")
        
    def stop_data_collection(self):
        self.start_watch = False

    def serial_error_handler(self):
        logger.debug(f"SharedDataCollectorClass serial_error_handler")
        self.errorOcurred.emit(True)
        

    def send_serial_message(self,message):
        # self.btSerialHandle.open_port()
        # self.serialHandleClass.open_port()
        self.btSerialHandle.send_message(message)
        # self.serialHandleClass.send_message(message)