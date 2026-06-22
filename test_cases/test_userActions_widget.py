from PySide6.QtCore import QObject, QByteArray, Signal, QTimer, Qt
from PySide6.QtTest import QSignalSpy

from shared_ui_modules.modules.db_functions import SharedDbClass
from shared_ui_modules.ui.model.stacked_widget_screens.user_actions_widget_model import SharedUserActionsModel

class FakeDb(SharedDbClass):
    def __init__(self):
        self.initialize_module()
    
    def get_db_name(self):
        return "test_db"

    def get_query_list(self):
        return ["""
            create table if not exists therapist (
                id integer primary key,
                name text not null,
                details text not null,
                image_path text
            );""","""
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
            values (1, 'paciente padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');""","""insert into therapist (id, name, details, image_path)
            values (1, 'terapeuta padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');"""]

class FakeLogModel(QObject):
    
    def __init__(self):
        super().__init__()

    def append_log(self,message):
        print(message)

class TestUserActions:
    
    def setup_method(self,method):
        print(f"TestUserActions")
        self.fake_log_model = FakeLogModel()
        self.db_class = FakeDb()
        self.user_actions_model = SharedUserActionsModel(dbHandleClass=self.db_class,logModel=self.fake_log_model)
        for q in ["delete from therapist;","delete from patient;","insert into patient (id, name, details, image_path) values (1, 'paciente padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');","insert into therapist (id, name, details, image_path) values (1, 'terapeuta padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');"]:
            self.db_class.execute_single_query(q=q)

    def test_new_patient_success(self,qtbot,monkeypatch):
        qtbot.wait(100)
        qtbot.addWidget(self.user_actions_model)

        #select patient tab
        # self.user_actions_model.tabWidget.setCurrentIndex(1)
        tab_bar = self.user_actions_model.tabWidget.tabBar()
        patient_tab_button_rect = tab_bar.tabRect(1).center()

        qtbot.mouseClick(
            tab_bar,
            Qt.LeftButton,
            pos = patient_tab_button_rect
        )
        
        assert self.user_actions_model.tabWidget.currentIndex() == 1

        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            self.user_actions_model.register_modal,
            "exec",
            lambda: None
        )

        self.user_actions_model.addPatientButton.click()

        self.user_actions_model.register_modal.nameEdit.setText("Name")
        self.user_actions_model.register_modal.descriptionEdit.setText("Description")

        assert self.user_actions_model.register_modal.infoDict["name"] == "Name"
        assert self.user_actions_model.register_modal.infoDict["details"] == "Description"

        self.user_actions_model.register_modal.accept()

        self.user_actions_model.addPatientButton.click()

        self.user_actions_model.register_modal.nameEdit.setText("Name")
        self.user_actions_model.register_modal.descriptionEdit.setText("Description")

        assert self.user_actions_model.register_modal.infoDict["name"] == "Name"
        assert self.user_actions_model.register_modal.infoDict["details"] == "Description"

        self.user_actions_model.register_modal.accept()

        qtbot.waitUntil(
            lambda: self.user_actions_model.patientListWidget.count() > 0
        )

        assert self.user_actions_model.patientListWidget.count() == 2

        #select the patient
        sigSPy_patientSelected = QSignalSpy(self.user_actions_model.patientSelected)
        
        patient_list_item_pos = self.user_actions_model.patientListWidget.visualItemRect(self.user_actions_model.patientListWidget.item(0))

        qtbot.mouseClick(
            self.user_actions_model.patientListWidget.viewport(),
            Qt.LeftButton,
            pos = patient_list_item_pos.center()
        )

        assert sigSPy_patientSelected.count() == 1
        
        qtbot.wait(100)

    def test_edit_patient_success(self,qtbot,monkeypatch):
        qtbot.addWidget(self.user_actions_model)

        #select patient tab
        # self.user_actions_model.tabWidget.setCurrentIndex(1)
        tab_bar = self.user_actions_model.tabWidget.tabBar()
        patient_tab_button_rect = tab_bar.tabRect(1).center()

        qtbot.mouseClick(
            tab_bar,
            Qt.LeftButton,
            pos = patient_tab_button_rect
        )

        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            self.user_actions_model.register_modal,
            "exec",
            lambda: None
        )

        self.user_actions_model.addPatientButton.click()

        self.user_actions_model.register_modal.nameEdit.setText("Name")
        self.user_actions_model.register_modal.descriptionEdit.setText("Description")

        self.user_actions_model.register_modal.accept()
        
        widget = self.user_actions_model.patientListWidget.itemWidget(self.user_actions_model.patientListWidget.item(0))
        
        qtbot.addWidget(widget)
                
        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            widget.register_modal,
            "exec",
            lambda: None
        )   
        
        widget.editButton.click()

        widget.register_modal.nameEdit.setText("EditedName")
        widget.register_modal.descriptionEdit.setText("EditedDescription")

        widget.register_modal.accept()

        res = self.db_class.execute_single_query("select (name, details) from patient where patient.id = ?;",[2])

        if res:
            assert res[0][0] == "EditedName"
            assert res[0][1] == "EditedDescription"

        qtbot.wait(100)

    def test_delete_patient_success(self,qtbot,monkeypatch):
        qtbot.addWidget(self.user_actions_model)

        #select patient tab
        # self.user_actions_model.tabWidget.setCurrentIndex(1)
        tab_bar = self.user_actions_model.tabWidget.tabBar()
        patient_tab_button_rect = tab_bar.tabRect(1).center()

        qtbot.mouseClick(
            tab_bar,
            Qt.LeftButton,
            pos = patient_tab_button_rect
        )

        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            self.user_actions_model.register_modal,
            "exec",
            lambda: None
        )

        self.user_actions_model.addPatientButton.click()

        self.user_actions_model.register_modal.nameEdit.setText("Name")
        self.user_actions_model.register_modal.descriptionEdit.setText("Description")

        self.user_actions_model.register_modal.accept()

        widget = self.user_actions_model.patientListWidget.itemWidget(self.user_actions_model.patientListWidget.item(0))
        
        qtbot.addWidget(widget)

        widget.removeButton.click()

        qtbot.waitUntil(
            lambda: self.user_actions_model.patientListWidget.count() == 0
        )

        assert self.user_actions_model.patientListWidget.count() == 0

        qtbot.wait(100)

    def test_new_therapist_success(self,qtbot,monkeypatch):
        qtbot.wait(100)
        qtbot.addWidget(self.user_actions_model)

        #select patient tab
        # self.user_actions_model.tabWidget.setCurrentIndex(1)
        tab_bar = self.user_actions_model.tabWidget.tabBar()
        patient_tab_button_rect = tab_bar.tabRect(0).center()

        qtbot.mouseClick(
            tab_bar,
            Qt.LeftButton,
            pos = patient_tab_button_rect
        )
        
        assert self.user_actions_model.tabWidget.currentIndex() == 0

        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            self.user_actions_model.register_modal,
            "exec",
            lambda: None
        )

        self.user_actions_model.addTherapistButton.click()

        self.user_actions_model.register_modal.nameEdit.setText("Name")
        self.user_actions_model.register_modal.descriptionEdit.setText("Description")

        assert self.user_actions_model.register_modal.infoDict["name"] == "Name"
        assert self.user_actions_model.register_modal.infoDict["details"] == "Description"

        self.user_actions_model.register_modal.accept()

        self.user_actions_model.addTherapistButton.click()

        self.user_actions_model.register_modal.nameEdit.setText("Name")
        self.user_actions_model.register_modal.descriptionEdit.setText("Description")

        assert self.user_actions_model.register_modal.infoDict["name"] == "Name"
        assert self.user_actions_model.register_modal.infoDict["details"] == "Description"

        self.user_actions_model.register_modal.accept()

        qtbot.waitUntil(
            lambda: self.user_actions_model.therapistListWidget.count() > 0
        )

        assert self.user_actions_model.therapistListWidget.count() == 2

        #select the patient
        sigSPy_therapistSelected = QSignalSpy(self.user_actions_model.therapistSelected)
        
        therapsit_list_item_pos = self.user_actions_model.therapistListWidget.visualItemRect(self.user_actions_model.therapistListWidget.item(0))

        qtbot.mouseClick(
            self.user_actions_model.therapistListWidget.viewport(),
            Qt.LeftButton,
            pos = therapsit_list_item_pos.center()
        )

        assert sigSPy_therapistSelected.count() == 1
        
        qtbot.wait(100)

    def test_edit_therapist_success(self,qtbot,monkeypatch):
        qtbot.wait(100)
        qtbot.addWidget(self.user_actions_model)

        #select patient tab
        # self.user_actions_model.tabWidget.setCurrentIndex(1)
        tab_bar = self.user_actions_model.tabWidget.tabBar()
        patient_tab_button_rect = tab_bar.tabRect(0).center()

        qtbot.mouseClick(
            tab_bar,
            Qt.LeftButton,
            pos = patient_tab_button_rect
        )
        
        assert self.user_actions_model.tabWidget.currentIndex() == 0

        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            self.user_actions_model.register_modal,
            "exec",
            lambda: None
        )

        self.user_actions_model.addTherapistButton.click()

        self.user_actions_model.register_modal.nameEdit.setText("Name")
        self.user_actions_model.register_modal.descriptionEdit.setText("Description")

        self.user_actions_model.register_modal.accept()
        
        widget = self.user_actions_model.therapistListWidget.itemWidget(self.user_actions_model.therapistListWidget.item(0))
        
        qtbot.addWidget(widget)
                
        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            widget.register_modal,
            "exec",
            lambda: None
        )   
        
        widget.editButton.click()

        widget.register_modal.nameEdit.setText("EditedName")
        widget.register_modal.descriptionEdit.setText("EditedDescription")

        widget.register_modal.accept()

        res = self.db_class.execute_single_query("select (name, details) from therapist where patient.id = ?;",[2])

        if res:
            assert res[0][0] == "EditedName"
            assert res[0][1] == "EditedDescription"

        qtbot.wait(100)

    def test_delete_therapist_success(self,qtbot,monkeypatch):
        qtbot.wait(100)
        qtbot.addWidget(self.user_actions_model)

        #select patient tab
        # self.user_actions_model.tabWidget.setCurrentIndex(1)
        tab_bar = self.user_actions_model.tabWidget.tabBar()
        patient_tab_button_rect = tab_bar.tabRect(0).center()

        qtbot.mouseClick(
            tab_bar,
            Qt.LeftButton,
            pos = patient_tab_button_rect
        )
        
        assert self.user_actions_model.tabWidget.currentIndex() == 0

        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            self.user_actions_model.register_modal,
            "exec",
            lambda: None
        )

        self.user_actions_model.addTherapistButton.click()

        self.user_actions_model.register_modal.nameEdit.setText("Name")
        self.user_actions_model.register_modal.descriptionEdit.setText("Description")

        self.user_actions_model.register_modal.accept()

        widget = self.user_actions_model.therapistListWidget.itemWidget(self.user_actions_model.therapistListWidget.item(0))
        
        qtbot.addWidget(widget)

        widget.removeButton.click()

        qtbot.waitUntil(
            lambda: self.user_actions_model.therapistListWidget.count() == 0
        )

        assert self.user_actions_model.therapistListWidget.count() == 0

        qtbot.wait(100)
