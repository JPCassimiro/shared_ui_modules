from shared_ui_modules.ui.views.calibration_widget_ui import Ui_calibrationForm
from shared_ui_modules.modules.log_class import logger

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, Signal, QCoreApplication, QEvent

class SharedCalibrationModel(QWidget):

    pValuesSignal = Signal(list)
    sideMenuDisableSignal = Signal(bool)
    
    def __init__(self,logModel,btSerialhandle):
        super().__init__()
        
        #setup ui
        self.ui = Ui_calibrationForm()
        self.ui.setupUi(self)
        
        #modules setup
        self.timer = QTimer()
        self.logModel = logModel
        self.btSerialhandle = btSerialhandle

        #variables
        self.step_2_pressure = [0]
        self.timeout_counter = 0
        self.calibration_step = 0
        self.string_list_instruction = []
        self.error_flag = False

        #get ui elements
        self.startButton = self.ui.startButton
        self.instructionText = self.ui.instructionLabel
        self.cancelButton = self.ui.cancelButton
        self.restartButton = self.ui.restartButton
        self.imgLabel = self.ui.imgLabel
        self.stackedWidget = self.ui.stackedWidget
        
        self.cancelButton.setEnabled(False)

        #connections
        self.startButton.clicked.connect(self.start_button_handler)
        self.timer.timeout.connect(self.timeout_handler)
        self.restartButton.clicked.connect(self.restart_calibration)
        self.cancelButton.clicked.connect(self.cancel_button_handler)
    
    def setup_model(self):
        #needs to be reasinged
        self.step_1_pressure = self.get_step_1_presusre()
        self.image_data = self.get_image_data()
        self.serial_messages = self.get_serial_messages()
        self.resultModel = self.get_result_model()
        self.stackedWidget.insertWidget(1,self.resultModel)
        self.set_translatable_strings()
        self.update_instruction_ui()
    
    def get_step_1_presusre(self):
        return 

    def get_image_data(self):
        return

    def get_serial_messages(self):
        return
    
    def get_str_array(self):
        return
    
    def get_result_model(self):
        return
    
    def set_translatable_strings(self):
        self.str_array = self.get_str_array()
        self.string_list_instruction = []
        for string in self.str_array:
            self.string_list_instruction.append(string)
            
    def set_instruction_image(self,img_path, width, height, radius = 0):
        try:
            img = QPixmap()
            if img.load(img_path):
                self.imgLabel.clear()
                self.imgLabel.setMinimumHeight(0)
                self.imgLabel.setMinimumWidth(0)
                self.imgLabel.setMaximumWidth(width)
                self.imgLabel.setMaximumHeight(height)
                if self.calibration_step == 0:
                    self.imgLabel.setMinimumWidth(width)
                    self.imgLabel.setMinimumHeight(height)
                self.imgLabel.radius = radius
                self.imgLabel.updateGeometry()
                self.imgLabel.setPixmap(img)
                self.imgLabel.setScaledContents(True)
            else:
                logger.error(f"Erro ao cerregar imagem no caminho: {img_path}")
        except Exception as e:
            logger.error(f"Erro ao atribuir uma imagem de instrução: {e}")
        
    def cancel_button_handler(self):
        self.timer.stop()
        self.timeout_counter = 0
        self.ui_counter = 0        
        if self.calibration_step == 0:
            self.step_1_pressure = [0]
        else:
            self.step_2_pressure = [0]
        self.cancelButton.setEnabled(False)
        self.restartButton.setEnabled(True)
        self.startButton.setEnabled(True)
        self.sideMenuDisableSignal.emit(True)
        self.btSerialhandle.mesReceivedSignal.disconnect(self.recieve_serial_message)
        self.btSerialhandle.port_error.disconnect(self.port_error_handle)
        self.error_flag = False
        
    #starts the timer
    #500ms timer for sending the messages
    def start_button_handler(self):
        self.startButton.setEnabled(False)
        self.restartButton.setEnabled(False)
        # self.serialHandleClass.mesReceivedSignal.connect(self.recieve_serial_message)
        self.btSerialhandle.mesReceivedSignal.connect(self.recieve_serial_message)
        self.btSerialhandle.port_error.connect(self.port_error_handle)
        self.cancelButton.setEnabled(True)
        self.timer.start(500)
        self.sideMenuDisableSignal.emit(False)
        self.error_flag = False

    def port_error_handle(self):
        self.logModel.append_log(f"Dispositivo não conectado")
        self.error_flag = True
        self.cancel_button_handler()
        
    #messages are to be sent in *S1 to *S4 order
    def send_serial_message(self,message):
        self.btSerialhandle.send_message(message)
    
    #messages will be recieved in the same order as they are sent, per serial rules
    def recieve_serial_message(self,recieved):
        self.logModel.append_log(recieved)
        if self.calibration_step == 0:
            self.handle_pressure_message_1(recieved)
        else:
            self.handle_pressure_message_2(recieved[:3])
        
    def handle_pressure_message_1(self, pressure):
        self.step_1_pressure.append(int(pressure[:3]))
    
    def handle_pressure_message_2(self, pressure):
        self.step_2_pressure.append(int(pressure[:3]))
        
    def restart_calibration(self):
        self.reset_variables()
        self.reset_screen()
        
    def reset_variables(self):
        self.step_1_pressure = [0]
        self.step_2_pressure = [0]
        self.timeout_counter = 0
        self.calibration_step = 0
        
    def reset_screen(self):
        # self.instructionText.setText(QCoreApplication.translate("InstructionText",self.string_list_instruction[1]))
        self.stackedWidget.setCurrentIndex(0)
        self.instructionText.show()
        self.imgLabel.show()
        self.update_instruction_ui()
        self.startButton.setEnabled(True)
        
    def present_results(self):
        self.imgLabel.hide()
        self.instructionText.hide()
        max_val_array = self.get_max_pressure_values()
        self.resultModel.set_pressure_values(max_val_array)
        self.stackedWidget.setCurrentIndex(1)
        self.startButton.setDisabled(True)
        
        #self.pValuesSignal.emit(max_val_array)
        
    def get_max_pressure_values(self):
        max_val_array = []
        if self.step_1_pressure:
            max_val_array.append(max(self.step_1_pressure))
            max_val_array.append(max(self.step_2_pressure))
            return max_val_array

    #11 timeouts in total
    #so 5.5 seconds total duration
    #first timer does nothing
    #starting from the second timer, or first timeout
        #sends 4 mesages
    #on final timeout
        #reenable screen
    def timeout_handler(self):
        if self.calibration_step == 0:
            if self.timeout_counter < 10:
                if len(self.serial_messages) > 2:
                    for m in self.serial_messages:
                        if self.error_flag == True:
                            break
                        self.send_serial_message(m)
                else:
                    self.send_serial_message(self.serial_messages[0])
                self.timeout_counter += 1
                return
            else:
                self.timeout_counter = 0
                self.startButton.setEnabled(True)
                self.restartButton.setEnabled(True)
                self.cancelButton.setEnabled(False)
                self.sideMenuDisableSignal.emit(True)
                # self.instructionText.setText(QCoreApplication.translate("InstructionText",self.string_list_instruction[1]))
                self.calibration_step = 1
                self.update_instruction_ui()
                self.timer.stop()
                self.btSerialhandle.mesReceivedSignal.disconnect(self.recieve_serial_message)
                self.btSerialhandle.port_error.disconnect(self.port_error_handle)
                # self.serialHandleClass.mesReceivedSignal.disconnect(self.recieve_serial_message)
                return
            
        elif self.calibration_step == 1:
            if self.timeout_counter < 10:
                self.send_serial_message(self.serial_messages[-1])
                self.timeout_counter += 1
                return
            else:
                self.timeout_counter = 0
                self.calibration_step = 0
                self.timer.stop()
                self.btSerialhandle.mesReceivedSignal.disconnect(self.recieve_serial_message)
                self.btSerialhandle.port_error.disconnect(self.port_error_handle)
                # self.serialHandleClass.mesReceivedSignal.disconnect(self.recieve_serial_message)
                self.startButton.setEnabled(True)
                self.restartButton.setEnabled(True)
                self.cancelButton.setEnabled(False)
                self.sideMenuDisableSignal.emit(True)
                self.present_results()
                return

    def update_instruction_ui(self):
        self.set_translatable_strings()
        img_array = self.image_data[self.calibration_step]
        img_info = []
        for info in img_array:
            img_info.append(info)
        if len(self.string_list_instruction) > 0:
            self.instructionText.setText(self.string_list_instruction[self.calibration_step])
        if len(img_info) == 4:
            self.set_instruction_image(img_path=img_info[0],width=img_info[1],height=img_info[2],radius=img_info[3])
        elif len(img_info) == 3:
            self.set_instruction_image(img_path=img_info[0],width=img_info[1],height=img_info[2])

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.update_instruction_ui()
        return super().changeEvent(event)