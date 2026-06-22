from .log_class import logger
from PySide6.QtCore import QProcess, Signal, QObject

class ProcessRunnerClass(QObject):
    processFinished = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        #process setup
        self.p = QProcess()

        #connecting funtions to signals
        self.p.finished.connect(self.process_finish_handler)
        self.p.errorOccurred.connect(self.process_error_handler)
        self.p.readyReadStandardError.connect(self.standard_error_read)
        
        self.error_flag = False#flag for errors, gets reset on run

    def run(self,argStr = None):
        self.error_flag = False
        try:
            if(argStr == None):
                self.processFinished.emit("Erro ao receber argumento")
                raise Exception("Erro ao receber argumentos")
            else:
                logger.debug(f"ProcessRunnerClass run QProcess iniciado:{argStr}")
                self.p.start(argStr[0],argStr[1])
                # self.p.kill()#!test line
        except Exception as e:
            logger.error(f"ProcessRunnerClass run\nErr: {e}\nArgStr: {argStr}")

    #read process stream
    def standard_error_read(self):
        try:
            data = self.p.readAllStandardError()
            stderr = bytes(data).decode("utf8")
            logger.debug(f"ProcessRunnerClass standard_error_read: {stderr}")
            self.error_flag = True
            self.p.kill()
        except Exception as e:
            logger.debug(f"ProcessRunnerClass standard_error_read error: {e}")

    #emits finish message
    def process_finish_handler(self):
        try:
            if self.error_flag == False:
                data = self.p.readAll()
                stderr = bytes(data).decode("utf8")
                logger.debug(f"ProcessRunnerClass process_finish_handler read: {stderr}")
                program = self.p.program()
                program = program.split("/")[-1]
                d = {}                    
                if program == "btdiscovery.exe":
                    arg_list = self.p.arguments()
                    mac = arg_list[4]
                    mac = mac[2:len(mac)-2]
                    d = {"status":True,"message":stderr,"mac":mac,"type":program}
                elif program == "btpair.exe" or program == "btdiscovery":
                    d = {"status":True,"message":"sucesso","type":program}
                self.processFinished.emit(d)
                logger.debug("QProcess finalizado")
        except Exception as e:
            logger.error(f"ProcessRunnerClass process_finish_handler error: {e}")
            
    def process_error_handler(self, error):
        d = {"message":f"Erro, verifique seu Joystick.","status":False}
        program = self.p.program()
        program = program.split("/")[-1]
        d["type"] = program
        if program == "btdiscovery.exe":
            arg_list = self.p.arguments()
            mac = arg_list[4]
            mac = mac[2:len(mac)-2]
            d["mac"] = mac
        self.processFinished.emit(d)
        logger.error(f"Erro no Qprocess\nErr: {error}\nArgs: {self.p.arguments()}\nProgram: {program}")

        