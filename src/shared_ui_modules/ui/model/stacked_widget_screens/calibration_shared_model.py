from shared_ui_modules.ui.views.calibration_widget_ui import Ui_calibrationForm
from shared_ui_modules.modules.log_class import logger

from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm
from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, Signal, QCoreApplication, QEvent

class SharedCalibrationModel(QWidget):

    pValuesSignal = Signal(list)
    sideMenuDisableSignal = Signal(bool)
    
    def __init__(self,logModel: SharedLogModel | None, btSerialhandle: SharedBtSerialComm | None):
        super().__init__()
        
        #setup ui
        self.ui = Ui_calibrationForm()
        self.ui.setupUi(self)
        
        #modules setup
        self.timer = QTimer()
        self.logModel = logModel
        self.btSerialhandle = btSerialhandle

        #watchers
        self._step_running_watcher = None

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

        #assing watcher
        self.step_running_watcher = False
    
    @property
    def step_running_watcher(self):
        return self._step_running_watcher

    @step_running_watcher.setter
    def step_running_watcher(self, status):
        self._step_running_watcher = status
        self.step_ui_watcher()

    def step_ui_watcher(self):
        try:
            if self._step_running_watcher == False:

                if self.stackedWidget.currentIndex() == 1:
                    self.cancelButton.setEnabled(False)
                    self.startButton.setEnabled(False)
                    self.restartButton.setEnabled(True)
                else:
                    self.cancelButton.setEnabled(False)
                    self.startButton.setEnabled(True)
                    if self.calibration_step == 0:
                        self.restartButton.setEnabled(False)
                    else:
                        self.restartButton.setEnabled(True)
                self.sideMenuDisableSignal.emit(True)
            else:
                self.cancelButton.setEnabled(True)
                self.restartButton.setEnabled(False)
                self.startButton.setEnabled(False)
                self.sideMenuDisableSignal.emit(False)
        except Exception as e:
            logger.error(f"SharedCalibrationModel step_ui_watcher error: {e}")
        
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
        try:
            self.str_array = self.get_str_array()
            self.string_list_instruction = []
            for string in self.str_array:
                self.string_list_instruction.append(string)
        except Exception as e:
            logger.error(f"SharedCalibrationModel set_translatable_strings error: {e}")
            
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
                raise Exception("load image error, path error")
        except Exception as e:
            logger.error(f"SharedCalibrationModel set_instruction_image error: {e}")
            raise
        
    def cancel_current_step(self):
        try:
            self.timer.stop()
            self.timeout_counter = 0
            if self.calibration_step == 0:
                self.step_1_pressure = self.get_step_1_presusre()
            else:
                self.step_2_pressure = [0]
            self.step_running_watcher = False
            self.btSerialhandle.mesReceivedSignal.disconnect(self.recieve_serial_message)
            self.btSerialhandle.port_error.disconnect(self.port_error_handle)
            self.error_flag = False
        except Exception as e:
            logger.error(f"SharedCalibrationModel cancel_current_step error: {e}")
            raise
            
    def cancel_button_handler(self):
        try:
            self.cancel_current_step()
        except Exception as e:
            logger.error(f"SharedCalibrationModel cancel_button_handler error: {e}")
    
    def start_callibration(self):
        try:
            self.step_running_watcher = True
            self.btSerialhandle.mesReceivedSignal.connect(self.recieve_serial_message)
            self.btSerialhandle.port_error.connect(self.port_error_handle)
            self.timer.start(500)
            self.error_flag = False
        except Exception as e:
            logger.error(f"SharedCalibrationModel start_callibration error: {e}")
            raise
            
    #starts the timer
    #500ms timer for sending the messages
    def start_button_handler(self):
        try:
            self.start_callibration()
        except Exception as e:
            logger.error(f"SharedCalibrationModel start_button_handler error: {e}")
        
    def port_error_handle(self):
        try:
            self.error_flag = True
            self.cancel_button_handler()
        except Exception as e:
            logger.error(f"SharedCalibrationModel port_error_handle error: {e}")
        
    #messages are to be sent in *S1 to *S4 order
    def send_serial_message(self,message):
        try:
            self.btSerialhandle.send_message(message)
        except Exception as e:
            logger.error(f"SharedCalibrationModel send_serial_message error: {e}")
    
    #messages will be recieved in the same order as they are sent, per serial rules
    def recieve_serial_message(self,recieved):
        try:
            if self.calibration_step == 0:
                self.handle_pressure_message_1(recieved)
            else:
                self.handle_pressure_message_2(recieved[:3])
        except Exception as e:
            logger.error(f"SharedCalibrationModel recieve_serial_message error: {e}")
        
    def handle_pressure_message_1(self, pressure):
        try:
            self.step_1_pressure.append(int(pressure[:3]))
        except Exception as e:
            logger.error(f"SharedCalibrationModel handle_pressure_message_1 error: {e}")
    
    def handle_pressure_message_2(self, pressure):
        try:
            self.step_2_pressure.append(int(pressure[:3]))
        except Exception as e:
            logger.error(f"SharedCalibrationModel handle_pressure_message_2 error: {e}")
        
    def restart_calibration(self):
        try:
            self.reset_variables()
            self.reset_screen()
        except Exception as e:
            logger.error(f"SharedCalibrationModel restart_calibration error: {e}")
        
    def reset_variables(self):
        try:
            self.step_1_pressure = self.get_step_1_presusre()
            self.step_2_pressure = [0]
            self.timeout_counter = 0
            self.calibration_step = 0
        except Exception as e:
            logger.error(f"SharedCalibrationModel reset_variables error: {e}")
            raise
        
    def reset_screen(self):
        try:
            # self.instructionText.setText(QCoreApplication.translate("InstructionText",self.string_list_instruction[1]))
            self.stackedWidget.setCurrentIndex(0)
            self.instructionText.show()
            self.imgLabel.show()
            self.update_instruction_ui()
            self.step_running_watcher = False
        except Exception as e:
            logger.error(f"SharedCalibrationModel reset_screen error: {e}")
            raise 
                    
    def present_results(self):
        try:
            self.imgLabel.hide()
            self.instructionText.hide()
            max_val_array = self.get_max_pressure_values()
            self.resultModel.set_pressure_values(max_val_array)
            self.stackedWidget.setCurrentIndex(1)
            self.startButton.setDisabled(True)
            #self.pValuesSignal.emit(max_val_array)
        except Exception as e:
            logger.error(f"SharedCalibrationModel present_results error: {e}")
            raise
        
    def get_max_pressure_values(self):
        try:
            max_val_array = []
            if self.step_1_pressure:
                max_val_array.append(max(self.step_1_pressure))
                max_val_array.append(max(self.step_2_pressure))
                return max_val_array
        except Exception as e:
            logger.error(f"SharedCalibrationModel reset_variables error: {e}")
            raise 
        
    #11 timeouts in total
    #so 5.5 seconds total duration
    #first timer does nothing
    #starting from the second timer, or first timeout
        #sends 4 mesages
    #on final timeout
        #reenable screen
    def step_0_timeout(self):
        try:
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
                self.step_end()
                return
        except Exception as e:
            logger.error(f"SharedCalibrationModel step_0_timeout error: {e}")
            raise
        
    def step_1_timeout(self):
        try:
            if self.timeout_counter < 10:
                self.send_serial_message(self.serial_messages[-1])
                self.timeout_counter += 1
                return
            else:
                self.step_end()
                return
        except Exception as e:
            logger.error(f"SharedCalibrationModel step_1_timeout error: {e}")
            raise

    def step_end(self):
        try:
            self.timeout_counter = 0
            self.timer.stop()
            self.btSerialhandle.mesReceivedSignal.disconnect(self.recieve_serial_message)
            self.btSerialhandle.port_error.disconnect(self.port_error_handle)
            if self.calibration_step == 0:
                self.calibration_step = 1
                self.update_instruction_ui()
            else:
                self.calibration_step = 0
                self.present_results()
            self.step_running_watcher = False
        except Exception as e:
            logger.error(f"SharedCalibrationModel step_1_timeout error: {e}")
            raise

    def timeout_handler(self):
        try:
            if self.calibration_step == 0:
                self.step_0_timeout()                
            elif self.calibration_step == 1:
                self.step_1_timeout()                
        except Exception as e:
            logger.error(f"SharedCalibrationModel timeout_handler error: {e}")

    def update_instruction_ui(self):
        try:
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
        except Exception as e:
            logger.error(f"SharedCalibrationModel update_instruction_ui error: {e}")

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.update_instruction_ui()
        return super().changeEvent(event)