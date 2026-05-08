from shared_ui_modules.ui.views.game_profile_widget_ui import Ui_gameProfileWidgetForm

from shared_ui_modules.modules.log_class import logger

from shared_ui_modules.ui.model.components.end_config_model import SharedEndConfigModel

from PySide6.QtWidgets import QWidget, QListWidgetItem, QMessageBox, QPushButton
from PySide6.QtCore import Qt, Signal, QCoreApplication, QEvent, QSize

import json

class SharedGameProfileModel(QWidget):

    to_config = Signal(object)

    def __init__(self, logModel, dbHandle, btSerialHandle):
        super().__init__()

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
        if not self._selected_profile:
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
        if self.selected_card:
            self.to_config_screen(self.selected_card.info_dict)

    def apply_all_configs_handle(self):
        if len(self.config_list) > 0:
            for config in self.config_list:
                bindindig_dict = config.info_dict 
                self.apply_config(bindindig_dict)

    def apply_selected_config_handle(self):
        if self.selected_card:
            binding_dict = self.selected_card.info_dict
            self.apply_config(binding_dict)
            self.selected_card = None


    def delete_game_profile_button(self):
        self.delete_game_profile()

    def card_select_handle(self,item):
        self.config_card_selection(item)

    def delete_buton_handle(self):
        self.delete_card()

    def new_card_button_handle(self):
        self.create_new_config()

    def new_profile_button_handle(self):
        if self.gameProfileLineEdit.text() != "":
            self.create_new_profile()
        else:
            self.handle_error_modal(QCoreApplication.translate("WarningText", "O campo do nome é obrigatório"))

    def profile_selection_handle(self,item):
        self.game_profile_selection(item)

    def config_card_selection(self,item):
        card = self.cardListWidget.itemWidget(item)
        self.selected_card = card

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
            self.selected_profile = None
            if len(self.profile_list) > 0:
                for profile in self.profile_list:
                    item = QListWidgetItem()
                    item.setText(profile[1])
                    item.setData(Qt.UserRole, profile[0])
                    item.setTextAlignment(Qt.AlignHCenter)
                    self.gameProfileList.addItem(item)
        except Exception as e:
            logger.error(f"erro ao atualizar lista: {e}")
                
    def read_json_file(self):
        data = self.jsonWriter.read_json_file("_internal/resources/latest_bindings/user_bindings.json")
        return data

    def create_new_config(self):
        try:
            config = self.read_json_file()

            q = """insert 
                    into bindings
                    (game_id, bindings_json)
                    values (?,?)
                    returning id;"""
                    
            logger.debug(f"create_new_config config:{config}")

            res = self.dbHandle.execute_single_query(q,[self.selected_profile.data(Qt.ItemDataRole.UserRole),str(config).replace("'","\"")])
            
            if res:
                logger.debug(f"nova config criada: {res[0]}")
                self.populate_config_list()
        except Exception as e:
            logger.debug(f"create_new_config error:{e}")
        
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
        except Exception as e:
            self.handle_error_modal(QCoreApplication.translate("WarningText", "Erro ao tentar criar um perfil"))
            
    def game_profile_selection(self,item):
        try:
            logger.debug(f"game_profile_selection item:{item.text()}")

            self.selected_profile = item
            self.selected_card = None
            self.populate_config_list()
        except Exception as e:
            self.handle_error_modal(QCoreApplication.translate("WarningText", "Erro ao selecionar um perfil"))
    
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
            logger.debug(f"populate_config_list error:{e}")
        
    def json_cleanup(self,bindings_text):
        data = json.loads(bindings_text)
        return data
    
    def delete_card(self):
        try:
            q = """
                delete from bindings where id = ? returning id;"""

            res = self.dbHandle.execute_single_query(q,[self.selected_card.id])

            if res:
                logger.debug(f"delete_card id:{res[0]}")
                self.populate_config_list()
                self.selected_card = None
        except Exception as e:
            logger.debug(f"delete_card error:{e}")
            
    def delete_game_profile(self):
        try:
            q = """
                delete from game_profile where id = ? returning id;"""

            res = self.dbHandle.execute_single_query(q,[self.selected_profile.data(Qt.ItemDataRole.UserRole)])

            if res:
                self.selected_profile = None
                self.populate_config_list()
                self.populate_game_profile_list()
                logger.debug(f"delete_game_profile id:{res[0]}")
        except Exception as e:
            logger.debug(f"delete_card error:{e}")
            
    def standardize_serial_message(self,binding_dict):
        messages = []

        logger.debug(f"standardize_serial_message binding_dict: {binding_dict}")

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

    def send_serial_message(self, message):
        try:
            if self.btSerialHandle.bt_socket != None:
                self.btSerialHandle.send_message(message)
        except Exception as e:
            logger.debug(f"send_serial_message error:{e}")
        
    def apply_config(self,config_dict):
        messages = self.standardize_serial_message(config_dict)
        self.end_modal.sent_message_total = len(messages)  
        self.btSerialHandle.mesReceivedSignal.connect(self.message_received_handler)
        for message in messages:
            self.send_serial_message(message)
        self.end_modal.exec()

    def to_config_screen(self, config):
        self.to_config.emit(config)
        
    def handle_error_modal(self, message):
        warning = QMessageBox(self)
        warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
        warning.setText(message)
        warning.setWindowModality(Qt.ApplicationModal)
        warning.show()

    def finish_modal(self):
        self.btSerialHandle.mesReceivedSignal.disconnect(self.message_received_handler)

    def message_received_handler(self,response):
        self.end_modal.recieve_end_message(response)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
        return super().changeEvent(event)