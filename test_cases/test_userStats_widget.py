
from shared_ui_modules.ui.model.stacked_widget_screens.user_stats_model import SharedUserStatsModel
from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm
from shared_ui_modules.modules.db_functions import SharedDbClass

from PySide6.QtCore import QObject, Signal, QByteArray

import pytestqt
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
            create table if not exists session (
                id integer primary key,
                patient_id integer not null,
                session_date timestamp not null default current_timestamp,
                foreign key (patient_id) references patient(id) on delete cascade
            );""","""
            create table if not exists use_data (
                id integer primary key,
                session_id integer not null,
                action text check(action in ('inhale','exhale')),
                pressure integer not null,
                timestamp datetime default current_timestamp,
                foreign key (session_id) references session(id) on delete cascade
            );""","""insert into patient (id, name, details, image_path)
            values (1, 'paciente padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');"""]

class FakeSocket(QObject):
    
    readyRead = Signal()
    
    def __init__(self):
        super().__init__()

        self.data = None

    def readAll(self):
        if self.data:
            return QByteArray(self.data)
    
    def isOpen(self):
        return True

class FakeLogModel(QObject):
    
    def __init__(self):
        super().__init__()

    def append_log(self,message):
        print(message)

class TestUserStatsWidget:
    
    def setup_method(self,method):
        self.db_class = FakeDb()
        self.fake_log_model = FakeLogModel()
        self.fake_socket = FakeSocket()
        self.btSerial_handle = SharedBtSerialComm()
        self.btSerial_handle.bt_socket = self.fake_socket
        self.stats_widget = SharedUserStatsModel(logModel=self.fake_log_model,btSerialHandle=self.btSerial_handle,)
        for q in ["delete from use_data","delete from session","delete from patient;","insert into patient (id, name, details, image_path) values (1, 'paciente padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');"]:
            self.db_class.execute_single_query(q=q)
            
    def test_get_current_timezone_success(self,qtbot):
        qtbot.addWidget(self.stats_widget)

        res = self.stats_widget.get_current_timezone()

        assert res == "-03:00"
    