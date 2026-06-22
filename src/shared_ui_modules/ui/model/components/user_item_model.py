from shared_ui_modules.ui.views.user_item_ui import Ui_userItemForm
from shared_ui_modules.ui.model.dialogs.register_model import RegisterModel

from shared_ui_modules.modules.log_class import logger

from shared_ui_modules.modules.db_functions import SharedDbClass

from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, Qt, QCoreApplication

import re

class UserItemModel(QWidget):
    
    updateList = Signal(int)
    update_finish = Signal(bool)
    delete_finish = Signal(bool)
    
    def __init__(self, infoDict: dict | None, DbHandleClass: SharedDbClass | None):
        super().__init__()
        
        #ui setup
        self.ui = Ui_userItemForm()
        self.ui.setupUi(self)
        
        self.register_modal = RegisterModel()
        
        self.dbHandleClass = DbHandleClass

        self.item_id = infoDict["id"]
        self.item_table = infoDict["table"]
        
        self.info_dict = infoDict.copy()
        
        #get elements
        self.imageLabel = self.ui.itemImageLabel
        self.nameLabel = self.ui.nameLabel
        self.functionLabel = self.ui.functionLabel
        self.removeButton = self.ui.removeButton
        self.editButton = self.ui.editButton
        
        self.imageLabel.setMaximumHeight(100)
        self.imageLabel.setMaximumWidth(100)
        
        self.fill_fields(infoDict)
        
        #connections
        self.removeButton.clicked.connect(self.remove_button_handler)
        self.editButton.clicked.connect(self.edit_button_handler)
        self.register_modal.accepted.connect(self.handle_modal_accept)
        
    def edit_button_handler(self):
        try:
            self.edit_info_modal_exec()
        except Exception as e:
            logger.error(f"UserItemModel edit_button_handler error: {e}")
    
    def remove_button_handler(self):
        try:
            self.remove_user()
        except Exception as e:
            logger.error(f"UserItemModel remove_button_handler error: {e}")
            self.delete_finish.emit(False)
        
    def fill_fields(self,infoDict):
        self.set_image(infoDict["image_path"])
        self.nameLabel.setText(infoDict["name"])
        self.functionLabel.setText(infoDict["details"])

    def set_image(self,img_path):
        try:
            img = QPixmap()
            if img.load(img_path):
                self.imageLabel.setPixmap(img)
                self.imageLabel.setScaledContents(True)
            else:
                logger.error(f"Erro ao cerregar imagem no caminho: {img_path}")
        except Exception as e:
            logger.error(f"Erro ao atribuir uma imagem na lista: {e}")
        
    def remove_user(self):
        try:
            q = f"delete from {self.item_table} where id = ? returning name;"
            res = self.dbHandleClass.execute_single_query(q,[self.item_id])
            if res: 
                logger.debug(f"{res[0][0]} removido")
                self.info_dict = None
                self.updateList.emit(self.item_id)
                self.delete_finish.emit(True)
        except Exception as e:
            logger.error(f"UserItemModel remove_user error: {e}")
            raise            
        
    def handle_modal_accept(self):
        try:
            self.edit_user()
        except Exception as e:
            logger.error(f"UserItemModel handle_modal_accept error: {e}")
            self.update_finish.emit(False)
        
    def edit_user(self):
        try:
            update_info = self.register_modal.infoDict.copy()
            rgx1 = True
            rgx2 = True
            if update_info["name"] != None: rgx1 = re.search("^\s*$",update_info["name"])
            if update_info["details"] != None: rgx2 = re.search("^\s*$",update_info["details"])
            if rgx1 == None and rgx2 == None:
                q = f"update {self.item_table} set name = ?, details = ?, image_path = ? where id = ? returning id;"
                res = self.dbHandleClass.execute_single_query(q,[update_info["name"],update_info["details"],update_info["image_path"],self.item_id])
                if res:
                    self.info_dict = update_info.copy()
                    logger.debug(f"info do id {res[0][0]} da tabela {self.item_table} foi atualizado")
                    self.updateList.emit(self.item_id)
                    self.update_finish.emit(True)
            else:
                warning = QMessageBox(self)
                warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
                warning.setText(QCoreApplication.translate("WarningText", "Preencha todos os campos obrigatórios"))

                warning.setWindowModality(Qt.ApplicationModal)
                warning.show()
                self.register_modal.reset_values()
        except Exception as e:
            logger.error(f"UserItemModel edit_user error: {e}")
            raise
        
    def edit_info_modal_exec(self):
        try:
            self.register_modal.infoDict = self.info_dict.copy()
            self.register_modal.complete_fields()
            self.register_modal.exec()
        except Exception as e:
            logger.error(f"UserItemModel edit_info_modal_exec error: {e}")
            raise