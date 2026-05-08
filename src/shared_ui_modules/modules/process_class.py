from .log_class import logger
from PySide6.QtCore import QProcess, Signal, QObject

import csv

class ProcessRunnerClass(QObject):
    processFinished = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        #process setup
        self.p = QProcess()

        #connecting funtions to signals
        self.p.finished.connect(self.process_finish_handler)
        self.p.errorOccurred.connect(self.process_error_handler)
        self.p.readyReadStandardError.connect(self.read_handler)
        
        self.error_flag = False#flag for errors, gets reset on run

    def run(self,argStr = None):
        self.error_flag = False
        try:
            if(argStr == None):
                self.processFinished.emit("Erro ao receber argumento")
                logger.error("Erro ao receber um argumento")
            else:
                logger.debug(f"QProcess iniciado:{argStr}")
                self.p.start(argStr[0],argStr[1])
        except Exception as e:
            logger.error(f"Erro ao rodar um QProcess\nErr: {e}\nArgStr: {argStr}")

    #read process stream
    def read_handler(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        logger.debug(f"read_handler: {stderr}")
        self.error_flag = True
        self.p.kill()

    #emits finish message
    def process_finish_handler(self):
        if self.error_flag == False:
            data = self.p.readAll()
            stderr = bytes(data).decode("utf8")
            logger.debug(f"process_finish_handler read: {stderr}")
            arg_list = self.p.arguments()
            if len(arg_list) >= 4:
                mac = arg_list[4]
                mac = mac[2:len(mac)-2]
                self.processFinished.emit({"status":True,"message":stderr,"mac":mac,"type":0})
            else:
                self.processFinished.emit({"status":True,"message":"sucesso","type":1})
            logger.debug("QProcess finalizado")

    def process_error_handler(self, error):
        self.processFinished.emit({"message":f"Erro, verifique seu Joystick. \nQProcess error: {error}","status":False})
        logger.error(f"Erro no Qprocess\nErr: {error}")

        