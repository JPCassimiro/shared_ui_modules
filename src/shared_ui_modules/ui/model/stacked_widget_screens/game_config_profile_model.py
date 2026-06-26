from shared_ui_modules.ui.views.game_profile_widget_ui import Ui_gameProfileWidgetForm

from shared_ui_modules.modules.log_class import logger
from shared_ui_modules.modules.db_functions import SharedDbClass
from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm

from shared_ui_modules.ui.model.components.end_config_model import SharedEndConfigModel
from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel

from PySide6.QtWidgets import QWidget, QListWidgetItem, QMessageBox, QPushButton
from PySide6.QtCore import Qt, Signal, QCoreApplication, QEvent, QSize

import json

class SharedGameProfileModel(QWidget):

    to_config = Signal(object)

    def __init__(self, logModel: SharedLogModel | None = None, dbHandle: SharedDbClass | None = None, btSerialHandle: SharedBtSerialComm | None = None):
        super().__init__()
        
        self.log_model_translatable_strings = [
            QCoreApplication.translate("LoggerWidgetText","Erro ao adicionar configuração ao perfil"),
            QCoreApplication.translate("LoggerWidgetText","Erro ao criar novo perfil"),
            QCoreApplication.translate("LoggerWidgetText","Novo perfil criado"),
            QCoreApplication.translate("LoggerWidgetText","Configuração adicionada ao perfil selecionado"),
            QCoreApplication.translate("LoggerWidgetText","Valores aplicados a tela de configuração"),
            QCoreApplication.translate("LoggerWidgetText","Erro ao adicionar a configuração ao perfil"),
            QCoreApplication.translate("LoggerWidgetText","Erro ao remover uma configuração do perfil selecionado"),
            QCoreApplication.translate("LoggerWidgetText","Erro ao excluir um perfil de configurações"),
            QCoreApplication.translate("LoggerWidgetText","Erro"),
            QCoreApplication.translate("LoggerWidgetText","Ocorreu um erro no processo, tente novamente")
        ]

        #module setup
        self.logModel = logModel
        self.dbHandle = dbHandle
        self.btSerialHandle = btSerialHandle
        self.jsonWriter = None

        #ui setup
        self.ui = Ui_gameProfileWidgetForm()
        self.ui.setupUi(self)

        #module setup
        self.end_modal = SharedEndConfigModel()
        
        #get ui elements
        self.gameProfileList = self.ui.gameProfileList
        self.addNewCardButton = self.ui.addNewCardButton
        self.gameProfileLineEdit = self.ui.gameProfileLineEdit
        self.newGameProfileButton = self.ui.newGameProfileButton
        self.cardListWidget = self.ui.cardListWidget
        self.deleteCardButton = self.ui.deleteCardButton
        self.deleteGameProfileButton = self.ui.deleteGameProfileButton
        self.applyAllCardsButton = self.ui.applyAllCardsButton
        self.applySelectedCardButton = self.ui.applySelectedCardButton
        self.applyAllCardsButton = self.ui.applyAllCardsButton
        self.sendToConfigScreenButton = self.ui.sendToConfigScreenButton
        
        #connection setup
        self.gameProfileList.itemClicked.connect(self.profile_selection_handle)
        self.newGameProfileButton.clicked.connect(self.new_profile_button_handle)
        self.addNewCardButton.clicked.connect(self.new_card_button_handle)
        self.deleteCardButton.clicked.connect(self.delete_buton_handle)
        self.cardListWidget.itemClicked.connect(self.card_select_handle)
        self.deleteGameProfileButton.clicked.connect(self.delete_game_profile_button)
        self.applySelectedCardButton.clicked.connect(self.apply_selected_config_handle)
        self.applyAllCardsButton.clicked.connect(self.apply_all_configs_handle)
        self.sendToConfigScreenButton.clicked.connect(self.send_to_config_screen_handle)
        self.end_modal.finished.connect(self.finish_modal)
        
        #variable setup
        self.profile_list = []
        self.config_list = []
        self.current_user = None
        self._selected_profile = None
        self._selected_card = None
        
        #ui setup
        self.selected_card = None
        self.selected_profile = None

    def get_config_card(self,args):
        return

    def get_json_writer(self):
        return

    def initialize_module(self):
        self.jsonWriter = self.get_json_writer()

    def standardize_serial_message(self,binding_dict):
        return

    @property
    def selected_profile(self):
        return self._selected_profile
     
    @selected_profile.setter
    def selected_profile(self, item):
        self._selected_profile = item
        self.config_list = []
        self.selected_profile_button_watcher()

    @property
    def selected_card(self):
        return self._selected_card
    
    @selected_card.setter
    def selected_card(self, item):
        self._selected_card = item
        self.selected_card_button_watcher()
    
    def selected_card_button_watcher(self):
        if len(self.config_list) > 0:
            if self._selected_card:
                for button in self.ui.cardButtonContainer.findChildren(QPushButton):
                    button.setEnabled(True)
            else:
                for button in self.ui.cardButtonContainer.findChildren(QPushButton):
                    button.setEnabled(True)
                self.applySelectedCardButton.setEnabled(False)
                self.deleteCardButton.setEnabled(False)
                self.sendToConfigScreenButton.setEnabled(False)
                self.cardListWidget.clearSelection()
        else:
            for button in self.ui.cardButtonContainer.findChildren(QPushButton):
                button.setEnabled(False)  
            self.addNewCardButton.setEnabled(True)
            
    #also gets called on delete card and update list
    def selected_profile_button_watcher(self):
        if self._selected_profile is None:
            #when no profile is selected disable everything
            for button in self.ui.cardButtonContainer.findChildren(QPushButton):
                button.setDisabled(True)
            self.deleteGameProfileButton.setDisabled(True)
        else:
            #when a profile is selected, enable add new, delete profile and apply all
            if len(self.config_list) > 0:
                self.applyAllCardsButton.setEnabled(True)
            self.deleteGameProfileButton.setEnabled(True)
            self.addNewCardButton.setEnabled(True)
            
    def send_to_config_screen_handle(self):
        try:
            if self.selected_card:
                if self.selected_card.info_dict is None:
                    raise Exception("dict nulo")
                self.to_config_screen(self.selected_card.info_dict)
        except Exception as e:
            logger.error(f"SharedGameProfileModel send_to_config_screen_handle error: {e}")
            self.error_ocurred_process_cancel(self.log_model_translatable_strings[9])

    def apply_all_configs_handle(self):
        try:
            if len(self.config_list) > 0:
                dict_list = []
                for d in self.config_list:
                    if d.info_dict is None:#d.info_dict is null
                        raise Exception("dict nulo")
                        break
                    else:
                        dict_list.append(d.info_dict)
                self.apply_config(dict_list)
        except Exception as e:
            self.error_ocurred_process_cancel(self.log_model_translatable_strings[9])
            logger.error(f"SharedProfileModel apply_all_configs_handle error: {e}")
            self.logModel.append_log(self.log_model_translatable_strings[5])

    def apply_selected_config_handle(self):
        try:
            if self.selected_card:
                binding_dict = self.selected_card.info_dict
                if binding_dict is None:
                    raise Exception("dict nulo")
                self.apply_config([binding_dict])
                self.selected_card = None
        except Exception as e:
            self.error_ocurred_process_cancel(self.log_model_translatable_strings[9])
            logger.error(f"SharedProfileModel apply_all_configs_handle error: {e}")
            self.logModel.append_log(self.log_model_translatable_strings[5])

    def delete_game_profile_button(self):
        try:
            if self.selected_profile is None:
                raise Exception("Perfil não selecionado")
            self.delete_game_profile()
        except Exception as e:
            self.logModel.append_log(self.log_model_translatable_strings[7])

    def card_select_handle(self,item):
        try:
            if item is None:
                raise Exception("Null item")
            self.config_card_selection(item)
        except Exception as e:
            logger.debug(f"SharedGameProfiel card_select_handle error: {e}")

    def delete_buton_handle(self):
        try:
            if self.selected_card is None:
                raise Exception("Null card")
            self.delete_card()
        except Exception as e:
            logger.debug(f"SharedGameProfiel delete_buton_handle error: {e}")

    def new_card_button_handle(self):
        try:
            if self.selected_profile is None:
                raise Exception("null profile")
            self.create_new_config()
        except Exception as e:
            logger.error(f"SharedGameProfile new_card_button_handle error: {e}")
            self.logModel.append_log(self.log_model_translatable_strings[0])

    def new_profile_button_handle(self):
        if self.gameProfileLineEdit.text() != "":
            self.create_new_profile()
        else:
            self.logModel.append_log(self.log_model_translatable_strings[1])
            self.handle_error_modal(QCoreApplication.translate("WarningText", "O campo do nome é obrigatório"))

    def profile_selection_handle(self,item):
        try:
            if item is None:
                raise Exception("profile selection null")
            self.game_profile_selection(item)
        except Exception as e:
            logger.error(f"SharedGameProfileModel profile_selection_handle error: {e}")
            self.handle_error_modal(QCoreApplication.translate("WarningText", "Erro ao selecionar um perfil"))

    def config_card_selection(self,item):
        try:
            if item is None:
                raise Exception("Null item")
            card = self.cardListWidget.itemWidget(item)
            self.selected_card = card
        except Exception as e:
            logger.error(f"SharedGameProfile config_card_selection error: {e}")
            raise

    def assing_user(self,user_index):
        self.current_user = user_index
        self.populate_game_profile_list()

    def get_profile_list(self):
        try:
            self.profile_list = []
            q = """select 
                        g.id, g.name
                        from game_profile as g
                        where g.patient_id = ?;"""
            res = self.dbHandle.execute_single_query(q,[self.current_user])

            if res:
                for profile in res:
                    self.profile_list.append([profile[0], profile[1]])
        except Exception as e:
            logger.error(f"erro ao obter lista de perfís: {e}")

    def populate_game_profile_list(self):
        try:
            self.gameProfileList.clear()
            self.get_profile_list()
            self.cardListWidget.clear()
            self.config_list = []
            if len(self.profile_list) > 0:
                for profile in self.profile_list:
                    item = QListWidgetItem()
                    item.setText(profile[1])
                    item.setData(Qt.UserRole, profile[0])
                    item.setTextAlignment(Qt.AlignHCenter)
                    self.gameProfileList.addItem(item)
            self.selected_card = None
            self.selected_profile = None
        except Exception as e:
            logger.error(f"erro ao atualizar lista: {e}")
            
    def read_json_file(self):
        try:
            data = self.jsonWriter.read_json_file("_internal/resources/latest_bindings/user_bindings.json")
            return data
        except Exception as e:
            logger.error(f"SharedGameProfile read_json_file error: {e}")

    def create_new_config(self):
        try:
            
            if self.selected_profile is None:
                raise Exception("null profile")
            
            config = self.read_json_file()

            q = """insert 
                    into bindings
                    (game_id, bindings_json)
                    values (?,?)
                    returning id;"""
                    
            res = self.dbHandle.execute_single_query(q,[self.selected_profile.data(Qt.ItemDataRole.UserRole),str(config).replace("'","\"")])
            
            if res:
                logger.debug(f"nova config criada: {res[0]}")
                self.populate_config_list()
                self.logModel.append_log(self.log_model_translatable_strings[3])
        except Exception as e:
            logger.error(f"create_new_config error:{e}")
            raise

    def create_new_profile(self):
        try:
            if self.gameProfileLineEdit.text() != "":

                q = """insert
                        into game_profile
                        (patient_id, name) 
                        values (?,?) 
                        returning id;"""

                res = self.dbHandle.execute_single_query(q,[self.current_user,self.gameProfileLineEdit.text()]) 

                if res:
                    logger.debug(f"novo perfil criado: {res[0]}")
                    self.populate_game_profile_list()
                    self.gameProfileLineEdit.clear()
                    self.logModel.append_log(self.log_model_translatable_strings[2])
        except Exception as e:
            logger.error(f"SharedGameProfileModel create_new_profile error: {e}")
            raise
            
    def game_profile_selection(self,item):
        try:
            logger.debug(f"game_profile_selection item:{item.text()}")

            self.selected_profile = item
            self.selected_card = None
            self.populate_config_list()
        except Exception as e:
            logger.debug(f"SharedGameProfileModel game_profile_selection error: {e}")
            raise
    
    def populate_config_list(self):
        try:
            self.cardListWidget.clear()
            self.config_list = []
            if self.selected_profile:
                q = """select
                        b.id, b.bindings_json 
                        from bindings as b
                        where b.game_id = ?;"""
                logger.debug(f"update_config_list selected_profile:{self.selected_profile.data(Qt.ItemDataRole.UserRole)}")
                res = self.dbHandle.execute_single_query(q,[self.selected_profile.data(Qt.ItemDataRole.UserRole)])

                if res:
                    for config in res:
                        bindings_dict = self.json_cleanup(config[1])
                        card = self.get_config_card([config[0], bindings_dict])
                        item_container = QListWidgetItem(self.cardListWidget)
                        item_container.setSizeHint(card.sizeHint())
                        self.cardListWidget.addItem(item_container)
                        self.cardListWidget.setItemWidget(item_container, card)
                        self.config_list.append(card)
                self.selected_profile_button_watcher()
        except Exception as e:
            logger.error(f"populate_config_list error: {e}")
            raise
        
    def json_cleanup(self,bindings_text):
        try:
            data = json.loads(bindings_text)
            return data
        except Exception as e:
            logger.error(f"SharedGameProfileModel json_cleanup error: {e}")
            raise
    
    def delete_card(self):
        try:
            if self.selected_card is None:
                raise Exception("null card")
            
            q = """
                delete from bindings where id = ? returning id;"""

            res = self.dbHandle.execute_single_query(q,[self.selected_card.id])

            if res:
                logger.debug(f"delete_card id:{res[0]}")
                self.populate_config_list()
                self.selected_card = None
        except Exception as e:
            logger.error(f"delete_card error:{e}")
            self.logModel.append_log(self.log_model_translatable_strings[5])
            raise
            
    def delete_game_profile(self):
        try:
            if self.selected_profile is None:
                raise Exception("Perfil não selecionado")

            q = """
                delete from game_profile where id = ? returning id;"""

            res = self.dbHandle.execute_single_query(q,[self.selected_profile.data(Qt.ItemDataRole.UserRole)])

            if res:
                self.selected_profile = None
                self.populate_config_list()
                self.populate_game_profile_list()
                logger.debug(f"delete_game_profile id:{res[0]}")
        except Exception as e:
            logger.error(f"delete_card error:{e}")
            raise
            
    def standardize_serial_message(self,binding_dict = None):
        try:
            if binding_dict != None:
                messages = []

                value = binding_dict["pressure"]
                valueStr = None
                if int(value) != 0:
                    valueStr = int(value)
                    if(int(value) < 10):#value always needs to be sent in a 3 digit format 
                        valueStr = f"00{int(value)}"
                    elif(int(value) < 100):
                        valueStr = f"0{int(value)}"

                messages.append("*M{}{}".format(binding_dict["action"], valueStr))
                
                if binding_dict["repeat"] == "True":
                    messages.append("*R1")
                else:
                    messages.append("*R0")
                
                if binding_dict["action"] == "1":
                    messages.append("*B" + binding_dict["key"])
                else:
                    messages.append("*U" + binding_dict["key"])
                
                messages.append("*T" + binding_dict["duration"])
                
                return messages
            else:
                raise Exception("dict nulo")
        except Exception as e:
            logger.error(f"SharedGameProfileModel error: {e}")
            raise

    def send_serial_message(self, message):
        try:
            if self.btSerialHandle.socket_none_check():
                raise Exception(f"null socket")
            self.btSerialHandle.send_message(message)
        except Exception as e:
            logger.error(f"send_serial_message error:{e}")
            raise
        
    def apply_config(self,config_dict_list):
        try:
            if self.btSerialHandle.socket_none_check():
               raise Exception(f"null socket") 

            if config_dict_list is None:
               raise Exception(f"null config dict") 
            
            messages = []

            for config_dict in config_dict_list:
                messages.extend(self.standardize_serial_message(config_dict))

            self.end_modal.sent_message_total = len(messages)
            self.btSerialHandle.mesReceivedSignal.connect(self.message_received_handler)
            
            for m in messages:
                self.send_serial_message(m)
                
            self.end_modal.exec()
        except Exception as e:
            logger.debug(f"SharedGameProfile apply_config - error: {e}")
            raise

    def to_config_screen(self, config):
        try:
            self.to_config.emit(config)
            self.logModel.append_log(self.log_model_translatable_strings[3])
        except Exception as e:
            logger.error(f"SharedGameProfileModel to_config_screen error: {e}")
            raise

    def handle_error_modal(self, message):
        if message:
            warning = QMessageBox(self)
            warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
            warning.setText(message)
            warning.setWindowModality(Qt.ApplicationModal)
            warning.show()

    def finish_modal(self):
        self.btSerialHandle.mesReceivedSignal.disconnect(self.message_received_handler)

    def message_received_handler(self,response):
        try:
            self.end_modal.recieve_end_message(response)
        except Exception as e:
            logger.error(f"SharedGameProfileModel message_received_handler error: {e}")

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.log_model_translatable_strings = [
                QCoreApplication.translate("LoggerWidgetText","Erro ao adicionar configuração ao perfil"),
                QCoreApplication.translate("LoggerWidgetText","Erro ao criar novo perfil"),
                QCoreApplication.translate("LoggerWidgetText","Novo perfil criado"),
                QCoreApplication.translate("LoggerWidgetText","Configuração adicionada ao perfil selecionado"),
                QCoreApplication.translate("LoggerWidgetText","Valores aplicados a tela de configuração"),
                QCoreApplication.translate("LoggerWidgetText","Erro ao adicionar a configuração ao perfil"),
                QCoreApplication.translate("LoggerWidgetText","Erro ao remover uma configuração do perfil selecionado"),
                QCoreApplication.translate("LoggerWidgetText","Erro ao excluir um perfil de configurações"),
                QCoreApplication.translate("LoggerWidgetText","Erro"),
                QCoreApplication.translate("LoggerWidgetText","Ocorreu um erro no processo, tente novamente")
            ]
            self.populate_config_list()
        return super().changeEvent(event)
    
    def error_ocurred_process_cancel(self,message = None):
        self.handle_error_modal(message)
        self.populate_game_profile_list()