from PySide6.QtCore import QObject, QByteArray, Signal, QTimer, Qt
from PySide6.QtTest import QSignalSpy
from PySide6.QtWidgets import QWidget

from shared_ui_modules.modules.db_functions import SharedDbClass
from shared_ui_modules.ui.model.stacked_widget_screens.game_config_profile_model import SharedGameProfileModel
from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm

from unittest.mock import Mock 

class FakeDb(SharedDbClass):
    def __init__(self):
        self.initialize_module()
    
    def get_db_name(self):
        return "test_db"

    def get_query_list(self):
        return ["""
            create table if not exists patient(
                id integer primary key,
                name text not null,
                details text not null,
                image_path text
            );""","""
            create table if not exists game_profile (
                id integer primary key,
                patient_id integer not null,
                name text not null,
                foreign key (patient_id) references patient(id) on delete cascade
            );""","""
            create table if not exists bindings (
                id integer primary key,
                game_id integer not null,
                bindings_json text not null,
                foreign key (game_id) references game_profile(id) on delete cascade
            );""","""insert into patient (id, name, details, image_path)
            values (1, 'paciente padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');"""]

class FakeLogModel(QObject):
    
    def __init__(self):
        super().__init__()

    def append_log(self,message):
        print(message)

class FakeJson(QObject):
    
    def read_json_file(self,path):
        return "stringtest"

class TestConfigProfile:
    
    def setup_method(self,method):
        self.db_class = FakeDb()
        self.fake_log_model = FakeLogModel()
        self.serialBtHandle = SharedBtSerialComm()
        self.game_profile = SharedGameProfileModel(btSerialHandle=self.serialBtHandle,logModel=self.fake_log_model,dbHandle=self.db_class)
        self.game_profile.get_config_card = self.get_config_card
        self.game_profile.jsonWriter = FakeJson()
        self.game_profile.current_user = 1
        self.game_profile.json_cleanup = self.json_cleanup 
        for q in ["delete from game_profile;","delete from bindings;","delete from therapist;","delete from patient;","insert into patient (id, name, details, image_path) values (1, 'paciente padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');"]:
            self.db_class.execute_single_query(q=q)

    def json_cleanup(self,message):
        return "stringtest"
    
    def get_config_card(self,args):
        widget = QWidget()
        widget.setObjectName("card_widget")
        widget.setMinimumHeight(100)
        widget.setMinimumWidth(100)
        widget.setMaximumHeight(100)
        widget.setMaximumWidth(100)
        return widget
    
    def test_create_new_profile_success(self,qtbot,monkeypatch):
        qtbot.wait(100)
        qtbot.addWidget(self.game_profile)

        self.game_profile.gameProfileLineEdit.setText("Profile 1")

        self.game_profile.newGameProfileButton.click()

        qtbot.waitUntil(
            lambda: self.game_profile.gameProfileList.count() > 0,
        )        

        assert self.game_profile.gameProfileList.count() == 1

        item = self.game_profile.gameProfileList.item(0)
        widget_pos = self.game_profile.gameProfileList.visualItemRect(item)

        sigSpy_item_clicked = QSignalSpy(self.game_profile.gameProfileList.itemClicked)
        
        assert item.text() == "Profile 1"

        qtbot.mouseClick(
            self.game_profile.gameProfileList.viewport(),
            Qt.LeftButton,
            pos = widget_pos.center()
        )
        
        assert sigSpy_item_clicked.count() > 0
        assert self.game_profile.selected_profile == item

        assert self.game_profile.addNewCardButton.isEnabled() == True
        
    def test_delete_profile_success(self,qtbot,monkeypatch):
        qtbot.wait(100)
        qtbot.addWidget(self.game_profile)

        self.game_profile.gameProfileLineEdit.setText("Profile 1")

        self.game_profile.newGameProfileButton.click()

        qtbot.waitUntil(
            lambda: self.game_profile.gameProfileList.count() > 0,
        )

        item = self.game_profile.gameProfileList.item(0)
        widget_pos = self.game_profile.gameProfileList.visualItemRect(item)

        qtbot.mouseClick(
            self.game_profile.gameProfileList.viewport(),
            Qt.LeftButton,
            pos = widget_pos.center()
        )

        self.game_profile.deleteGameProfileButton.click()

        assert self.game_profile.gameProfileList.count() == 0
        assert self.game_profile.selected_profile == None

    # def test_add_config_to_profile_success(self,qtbot,monkeypatch):
    #     qtbot.wait(100)
    #     qtbot.addWidget(self.game_profile)

    #     self.game_profile.gameProfileLineEdit.setText("Profile 1")

    #     self.game_profile.newGameProfileButton.click()

    #     qtbot.waitUntil(
    #         lambda: self.game_profile.gameProfileList.count() > 0,
    #     )
        
    #     item = self.game_profile.gameProfileList.item(0)
    #     widget_pos = self.game_profile.gameProfileList.visualItemRect(item)

    #     qtbot.mouseClick(
    #         self.game_profile.gameProfileList.viewport(),
    #         Qt.LeftButton,
    #         pos = widget_pos.center()
    #     )
        
    #     self.game_profile.addNewCardButton.click()

    #     qtbot.waitUntil(
    #         lambda: self.game_profile.cardListWidget.count() > 0
    #     )

    #     card_item = self.game_profile.cardListWidget.itemWidget(self.game_profile.cardListWidget.item(0))
        
    #     print(f"card_item.objectName(): {card_item.objectName()}")
        
    #     sigSpy_card_list_clicked = QSignalSpy(self.game_profile.cardListWidget.itemClicked)

    #     qtbot.mouseClick(
    #         card_item,
    #         Qt.LeftButton
    #     )

    #     qtbot.waitUntil(
    #         lambda: self.game_profile.selected_card is not None
    #     )

    def test_standardize_serial_message_function_success(self,qtbot,monkeypatch):
        d = {"pressure":100,"repeat":"True","action":"1","duration":"0","key":"A"}
        res = self.game_profile.standardize_serial_message(d)

        assert res[0] == f"*M{d['action']}100"
        assert res[1] == f"*R1"
        assert res[2] == f"*BA"
        assert res[3] == f"*T0"

        d = {"pressure":100,"repeat":"True","action":"1","duration":"0","key":"A"}
        res = self.game_profile.standardize_serial_message(d)

        assert res[0] == f"*M1100"
        assert res[1] == f"*R1"
        assert res[2] == f"*BA"
        assert res[3] == f"*T0"
        