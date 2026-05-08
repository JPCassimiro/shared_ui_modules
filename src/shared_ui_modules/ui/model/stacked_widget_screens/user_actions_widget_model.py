from shared_ui_modules.ui.views.user_actions_widget_ui import Ui_usersWidgetForm
from shared_ui_modules.ui.model.dialogs.register_model import RegisterModel
from shared_ui_modules.ui.model.components.user_item_model import UserItemModel

from PySide6.QtWidgets import QWidget, QListWidgetItem, QMessageBox
from PySide6.QtCore import Signal, Qt, QEvent, QCoreApplication

import re

class SharedUserActionsModel(QWidget):
    
    therapistSelected = Signal(dict)    
    patientSelected = Signal(dict)    

    def __init__(self, dbHandleClass):
        super().__init__()
        
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
        self.listWidget1 = self.ui.listWidget1
        self.lineEdit1 = self.ui.lineEdit1
        self.toolButton1 = self.ui.toolButton1
        self.listWidget2 = self.ui.listWidget2
        self.lineEdit2 = self.ui.lineEdit2
        self.toolButton2 = self.ui.toolButton2
        self.defaultPatientButton = self.ui.defaultPatientButton
        self.defautlTherapistButton = self.ui.defautlTherapistButton
        
        self.lineEdit1.setProperty("type",0)
        self.lineEdit2.setProperty("type",1)
        self.toolButton1.setProperty("type",0)
        self.toolButton2.setProperty("type",1)
        self.listWidget1.setProperty("type",0)
        self.listWidget2.setProperty("type",1)
        
        self.lineEdit1.hide()
        self.lineEdit2.hide()

        #connections
        self.toolButton1.clicked.connect(self.add_button_handler)
        self.toolButton2.clicked.connect(self.add_button_handler)
        self.register_modal.accepted.connect(self.register_user)
        self.defautlTherapistButton.clicked.connect(self.select_default_therapist)
        self.defaultPatientButton.clicked.connect(self.select_default_patient)
        
        self.listWidget1.clicked.connect(self.get_user)
        self.listWidget2.clicked.connect(self.get_user)
        
        self.populate_lists()

        self.default_p_dict, self.default_t_dict = self.get_default_users()

        self.register_modal.setWindowModality(Qt.ApplicationModal)
        
        #style adjustments
        self.listWidget1.setSpacing(5)
        self.listWidget2.setSpacing(5)

    def select_default_patient(self):
        signal_dict_p = self.default_p_dict.copy()
        self.patientSelected.emit(signal_dict_p)

    def select_default_therapist(self):
        signal_dict_t = self.default_t_dict.copy()
        self.therapistSelected.emit(signal_dict_t)

    def assin_default_user(self):
        signal_dict_p = self.default_p_dict.copy()
        signal_dict_t = self.default_t_dict.copy()
        self.patientSelected.emit(signal_dict_p)
        self.therapistSelected.emit(signal_dict_t)

    def get_default_users(self):
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
        

    def add_button_handler(self):
        if self.sender().property("type") == 0:
            self.register_modal.current_table = "therapist"
        else:
            self.register_modal.current_table = "patient"
        self.register_modal.exec()

    #also creates a session on the current timestamp so the user_stats widget dosent break
    def register_user(self):
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
                self.register_modal.reset_values()
                self.visually_update_list()
  
        else:
            warning = QMessageBox(self)
            warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
            warning.setText(QCoreApplication.translate("WarningText", "Preencha todos os campos obrigatórios"))
            warning.setWindowModality(Qt.ApplicationModal)
            warning.show()
            self.register_modal.reset_values()
        
    def visually_update_list(self):
        self.listWidget1.clear()
        self.listWidget2.clear()
        self.populate_lists()

    def update_list_handler(self,itemId):
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
            
    def get_user(self,index):
        item = self.sender().item(index.row())
        widget = self.sender().itemWidget(item)
        signal_dict = widget.info_dict.copy()
        if self.sender().property("type") == 0:
            self.therapistSelected.emit(signal_dict)
            self.current_therapist = widget.item_id
        else:
            self.patientSelected.emit(signal_dict)
            self.current_patient = widget.item_id

    def populate_lists(self):
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
                    item_container = QListWidgetItem(self.listWidget1)
                    item_container.setSizeHint(item.sizeHint())                
                    self.listWidget1.addItem(item_container)
                    self.listWidget1.setItemWidget(item_container,item)
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
                    item_container = QListWidgetItem(self.listWidget2)
                    item_container.setSizeHint(item.sizeHint())                
                    self.listWidget2.addItem(item_container)
                    self.listWidget2.setItemWidget(item_container,item)
                    
    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
        return super().changeEvent(event)
        

    
        