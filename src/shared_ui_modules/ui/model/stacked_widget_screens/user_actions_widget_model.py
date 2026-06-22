from shared_ui_modules.ui.views.user_actions_widget_ui import Ui_usersWidgetForm
from shared_ui_modules.ui.model.dialogs.register_model import RegisterModel
from shared_ui_modules.ui.model.components.user_item_model import UserItemModel

from shared_ui_modules.modules.db_functions import SharedDbClass
from shared_ui_modules.modules.log_class import logger

from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel

from PySide6.QtWidgets import QWidget, QListWidgetItem, QMessageBox
from PySide6.QtCore import Signal, Qt, QEvent, QCoreApplication

import re

class SharedUserActionsModel(QWidget):
    
    therapistSelected = Signal(dict)    
    patientSelected = Signal(dict)    

    def __init__(self, dbHandleClass: SharedDbClass | None = None, logModel: SharedLogModel | None = None ):
        super().__init__()

        self.logModel = logModel
        
        self.log_model_translatable_strings = [
            QCoreApplication.translate("LoggerWidgetText","Cadastro realizado com sucesso"),
            QCoreApplication.translate("LoggerWidgetText","Alteração realizada com sucesso"),
            QCoreApplication.translate("LoggerWidgetText","Remoção realizada com sucesso"),
            QCoreApplication.translate("LoggerWidgetText","Paciente selecionado:"),
            QCoreApplication.translate("LoggerWidgetText","Terapeuta selecionado:"),
            QCoreApplication.translate("LoggerWidgetText","Paciente padrão selecionado"),
            QCoreApplication.translate("LoggerWidgetText","Terapeuta padrão selecionado"),
            QCoreApplication.translate("LoggerWidgetText","Erro no processo de cadastro"),
            QCoreApplication.translate("LoggerWidgetText","Erro na alteração"),
            QCoreApplication.translate("LoggerWidgetText","Erro na remoção"),
            QCoreApplication.translate("LoggerWidgetText","Erro ao selecionar um cadastro")
        ]
        
        #setup ui
        self.ui = Ui_usersWidgetForm()
        self.ui.setupUi(self)
        
        #setup modules
        self.dbHandleClass = dbHandleClass
        
        #setup aditional components
        self.register_modal = RegisterModel()
        
        #variables
        self.current_therapist = None
        self.current_patient = None

        #get ui elements
        self.tabWidget = self.ui.tabWidget
        self.therapistListWidget = self.ui.therapistListWidget
        self.therapistLineEdit = self.ui.therapistLineEdit
        self.addTherapistButton = self.ui.addTherapistButton
        self.patientListWidget = self.ui.patientListWidget
        self.patientLineEdit = self.ui.patientLineEdit
        self.addPatientButton = self.ui.addPatientButton
        self.defaultPatientButton = self.ui.defaultPatientButton
        self.defautlTherapistButton = self.ui.defautlTherapistButton
        
        self.therapistLineEdit.setProperty("type",0)
        self.patientLineEdit.setProperty("type",1)
        self.addTherapistButton.setProperty("type",0)
        self.addPatientButton.setProperty("type",1)
        self.therapistListWidget.setProperty("type",0)
        self.patientListWidget.setProperty("type",1)
        
        self.therapistLineEdit.hide()
        self.patientLineEdit.hide()

        #connections
        self.addTherapistButton.clicked.connect(self.add_button_handler)
        self.addPatientButton.clicked.connect(self.add_button_handler)
        self.register_modal.accepted.connect(self.handle_modal_accept)
        self.defautlTherapistButton.clicked.connect(self.default_therapist_button_handler)
        self.defaultPatientButton.clicked.connect(self.default_patient_button_handler)
        
        self.therapistListWidget.clicked.connect(self.list_item_clicked_handler)
        self.patientListWidget.clicked.connect(self.list_item_clicked_handler)
        
        self.populate_lists()

        self.default_p_dict, self.default_t_dict = self.get_default_users()

        self.register_modal.setWindowModality(Qt.ApplicationModal)
        
        #style adjustments
        self.therapistListWidget.setSpacing(5)
        self.patientListWidget.setSpacing(5)
        
    def handle_modal_accept(self):
        try:
            self.register_modal.text_normalization()
            self.register_user()
        except Exception as e:
            logger.error(f"SharedUserActions handle_modal_accept error: {e}")
            self.logModel.append_log(self.log_model_translatable_strings[7])

    def default_patient_button_handler(self):
        try:
            self.select_default_patient()
        except Exception as e:
            logger.error(f"SharedUserActions default_patient_button_handler error: {e}")

    def default_therapist_button_handler(self):
        try:
            self.select_default_therapist()
        except Exception as e:
            logger.error(f"SharedUserActions default_therapist_button_handler error: {e}")

    def select_default_patient(self):
        try:
            signal_dict_p = self.default_p_dict.copy()
            self.patientSelected.emit(signal_dict_p)
            self.logModel.append_log(self.log_model_translatable_strings[5])
        except Exception as e:
            logger.error(f"SharedUserActions select_default_patient error: {e}")
            raise

    def select_default_therapist(self):
        try:
            signal_dict_t = self.default_t_dict.copy()
            self.therapistSelected.emit(signal_dict_t)
            self.logModel.append_log(self.log_model_translatable_strings[6])
        except Exception as e:
            logger.error(f"SharedUserActions select_default_therapist error: {e}")
            raise

    def assin_default_user(self):
        signal_dict_p = self.default_p_dict.copy()
        signal_dict_t = self.default_t_dict.copy()
        self.patientSelected.emit(signal_dict_p)
        self.therapistSelected.emit(signal_dict_t)

    def get_default_users(self):
        try:
            qPatient = f"select * from patient where id = 1;"
            qTherapist = f"select * from therapist where id = 1;"
            resP = self.dbHandleClass.execute_single_query(qPatient)
            resT = self.dbHandleClass.execute_single_query(qTherapist)
            p_dict = {}
            t_dict = {}
            if resP:
                p_dict = {
                    "id": resP[0][0],
                    "name": resP[0][1],
                    "details": resP[0][2],
                    "image_path": resP[0][3],
                }

            if resT:
                t_dict = {
                    "id": resT[0][0],
                    "name": resT[0][1],
                    "details": resT[0][2],
                    "image_path": resT[0][3],
                }

            return p_dict, t_dict
        except Exception as e:
            logger.error(f"SharedUserActions get_default_users error: {e}")
        
    def add_button_handler(self):
        try:
            if self.sender().property("type") == 0:
                self.register_modal.current_table = "therapist"
            else:
                self.register_modal.current_table = "patient"
            self.register_modal.exec()
        except Exception as e:
            logger.error(f"SharedUserActions add_button_handler error: {e}")

    #also creates a session on the current timestamp so the user_stats widget dosent break
    def register_user(self):
        try:
            register_info = self.register_modal.infoDict.copy()
            rgx1 = True
            rgx2 = True
            if register_info["name"] != None: rgx1 = re.search("^\s*$",register_info["name"])
            if register_info["details"] != None: rgx2 = re.search("^\s*$",register_info["details"])
            if rgx1 == None and rgx2 == None:
                q = ""
                q = f"insert into {self.register_modal.current_table} (name,details,image_path) values (?,?,?) returning id;"
                res = self.dbHandleClass.execute_single_query(q,[register_info["name"],register_info["details"],register_info["image_path"]])
                if res: 
                    self.logModel.append_log(self.log_model_translatable_strings[0])
                    self.register_modal.reset_values()
                    self.visually_update_list()
            else:
                warning = QMessageBox(self)
                warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
                warning.setText(QCoreApplication.translate("WarningText", "Preencha todos os campos obrigatórios"))
                warning.setWindowModality(Qt.ApplicationModal)
                warning.show()
                self.register_modal.reset_values()
        except Exception as e:
            logger.error(f"SharedUserActions register_user error: {e}")
            raise
        
    def visually_update_list(self):
        try:
            self.therapistListWidget.clear()
            self.patientListWidget.clear()
            self.populate_lists()
        except Exception as e:
            logger.error(f"SharedUserActions visually_update_list error: {e}")
            raise

    def update_list_handler(self,itemId):
        try:
            if itemId == self.current_patient:
                if self.sender().info_dict == None:
                    signal_dict = self.default_p_dict.copy()
                else:
                    signal_dict = self.sender().info_dict.copy()
                self.patientSelected.emit(signal_dict)
            elif itemId == self.current_therapist:
                if self.sender().info_dict == None:
                    signal_dict = self.default_t_dict.copy()
                else:
                    signal_dict = self.sender().info_dict.copy()
                self.therapistSelected.emit(signal_dict)
            self.visually_update_list()
        except Exception as e:
            logger.error(f"SharedUserActionsModel update_list_handler error: {e}")
            raise
            
    def list_item_clicked_handler(self,index):
        try:
            self.get_user(index)
        except Exception as e:
            logger.error(f"SharedUserActionsModel update_list_handler error: {e}")
            self.logModel.append_log(self.log_model_translatable_strings[10])

    def get_user(self,index):
        try:
            item = self.sender().item(index.row())
            widget = self.sender().itemWidget(item)
            signal_dict = widget.info_dict.copy()
            if self.sender().property("type") == 0:
                self.therapistSelected.emit(signal_dict)
                self.current_therapist = widget.item_id
                self.logModel.append_log(f"{self.log_model_translatable_strings[4]} {signal_dict["name"]}")
            else:
                self.patientSelected.emit(signal_dict)
                self.current_patient = widget.item_id
                self.logModel.append_log(f"{self.log_model_translatable_strings[3]} {signal_dict["name"]}")
        except Exception as e:
            logger.error(f"SharedUserActionsModel get_user error: {e}")
            raise

    def populate_lists(self):
        try:
            q_patient = f"select * from patient;"
            q_therapist = f"select * from therapist;"
            res_patient = self.dbHandleClass.execute_single_query(q_patient)
            res_therapist = self.dbHandleClass.execute_single_query(q_therapist)
            if res_therapist:
                for therapist in res_therapist:
                    if therapist[0] != 1:
                        infoDict = {
                            "id": therapist[0],
                            "name": therapist[1],
                            "details": therapist[2],
                            "image_path": therapist[3],
                            "table": "therapist"
                        }
                        item = UserItemModel(infoDict,self.dbHandleClass)
                        item.updateList.connect(self.update_list_handler)
                        item_container = QListWidgetItem(self.therapistListWidget)
                        item_container.setSizeHint(item.sizeHint())                
                        self.therapistListWidget.addItem(item_container)
                        self.therapistListWidget.setItemWidget(item_container,item)
            if res_patient: 
                for patient in res_patient:
                    if patient[0] != 1:
                        infoDict = {
                            "id": patient[0],
                            "name": patient[1],
                            "details": patient[2],
                            "image_path": patient[3],
                            "table": "patient"
                        }
                        item = UserItemModel(infoDict,self.dbHandleClass)
                        item.updateList.connect(self.update_list_handler)
                        item_container = QListWidgetItem(self.patientListWidget)
                        item_container.setSizeHint(item.sizeHint())                
                        self.patientListWidget.addItem(item_container)
                        self.patientListWidget.setItemWidget(item_container,item)
        except Exception as e:
            logger.error(f"SharedUserActionsModel populate_lists error: {e}")
            raise

    def delete_finish_handler(self,res: bool):
        if res == True:
            self.logModel.append_log(self.log_model_translatable_strings[2])
        elif res == False:
            self.logModel.append_log(self.log_model_translatable_strings[9])
        
    def update_finish_handler(self, res: bool):
        if res == True:
            self.logModel.append_log(self.log_model_translatable_strings[1])
        elif res == False:
            self.logModel.append_log(self.log_model_translatable_strings[8])
                  
    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.log_model_translatable_strings = [
                QCoreApplication.translate("LoggerWidgetText","Cadastro realizado com sucesso"),
                QCoreApplication.translate("LoggerWidgetText","Alteração realizada com sucesso"),
                QCoreApplication.translate("LoggerWidgetText","Remoção realizada com sucesso"),
                QCoreApplication.translate("LoggerWidgetText","Paciente selecionado:"),
                QCoreApplication.translate("LoggerWidgetText","Terapeuta selecionado:"),
                QCoreApplication.translate("LoggerWidgetText","Paciente padrão selecionado"),
                QCoreApplication.translate("LoggerWidgetText","Terapeuta padrão selecionado"),
                QCoreApplication.translate("LoggerWidgetText","Erro no processo de cadastro"),
                QCoreApplication.translate("LoggerWidgetText","Erro na alteração"),
                QCoreApplication.translate("LoggerWidgetText","Erro na remoção")
        ]
        return super().changeEvent(event)
        

    
        