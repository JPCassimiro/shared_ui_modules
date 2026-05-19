from shared_ui_modules.modules.desktop_services import DekstopServicesClass
from shared_ui_modules.modules.db_functions import SharedDbClass
from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm


from PySide6.QtWidgets import QWidget, QPushButton, QRadioButton, QMessageBox
from shared_ui_modules.modules.log_class import logger
from PySide6.QtCore import Signal, Qt, QCoreApplication, QEvent

import pyqtgraph as pg
import numpy as np
from pathlib import Path
from unidecode import unidecode

class SharedUserStatsModel(QWidget):

    def __init__(self,dbHandleClass: SharedDbClass | None = None, btSerialHandle: SharedBtSerialComm | None = None, logModel = None):
        super().__init__()

        self.btSerialHandle = btSerialHandle
        self.dbHandleClass = dbHandleClass

    def initialize_modules(self):
        #connections setup
        self.startListening.clicked.connect(self.start_button_handler)
        self.stopListening.clicked.connect(self.stop_button_handler)
        self.sessionComboBox.currentIndexChanged.connect(self.comboBox_change_handler)
        self.statsTabWidget.tabBarClicked.connect(self.update_summary_charts)
        self.newSessionButton.clicked.connect(self.new_session_button_handler)
        self.deleteSessionButton.clicked.connect(self.delete_session_handler)
        self.exportSessionCSVButton.clicked.connect(self.export_session_handler)
        self.csvWriter.exportEnd.connect(self.end_export_handle)
        self.csvWriter.exportError.connect(self.error_export_handle)
        self.dataCollectorHandler.errorOcurred.connect(self.data_collection_error_handle)
        self.exportSessionImageButton.clicked.connect(self.export_as_image_handler)
        self.set_dialog_text()

    def data_collection_error_handle(self):
        try:
            if self.dataCollectorHandler.start_watch == True:
                self.stop_button_handler()
            # elif self.dataCollectorHandler.start_watch = False
                # self.stop_button_handler()
        except Exception as e:
            logger.debug(f"SharedUserStatsModel data_collection_error_handler error: {e}")
        
    def end_export_handle(self, folder_path = None):
        try:
            warning = QMessageBox(self)
            warning.setWindowTitle(QCoreApplication.translate("WarningText", "Sucesso"))
            warning.setText(QCoreApplication.translate("WarningText", "Exportação realizada com sucesso. A pasta criada será aberta."))
            warning.setWindowModality(Qt.ApplicationModal)
            warning.show()
            if folder_path:
                DekstopServicesClass().open_folder(folder_path)
        except Exception as e:
            logger.debug(f"SharedUserStatsModel end_export_handle error: {e}")

    def error_export_handle(self):
        try:
            warning = QMessageBox(self)
            warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
            warning.setText(QCoreApplication.translate("WarningText", "Erro na exportação"))
            warning.setWindowModality(Qt.ApplicationModal)
            warning.show()
        except Exception as e:
            logger.debug(f"SharedUserStatsModel error_export_handle error: {e}")

    def delete_charts(self):
        try:
            self.summary_chart_layout_widget.deleteLater()
            self.session_chart_layout_widget.deleteLater()
            # self.ui.sessionChartContainer.layout().removeWidget(self.session_chart_layout_widget)
            # self.ui.summaryChartContainer.layout().removeWidget(self.summary_chart_layout_widget)
        except Exception as e:
            logger.debug(f"SharedUserStatsModel delete_charts error: {e}")

    def delete_session_handler(self):
        try:
            def on_accept():
                current_index = self.sessionComboBox.currentData()
                q = f"""delete from session where id = ? and patient_id = ? returning id;"""
                res = self.dbHandleClass.execute_single_query(q,[current_index,self.current_user])
                self.populate_comboBox()
                if res:
                    deletionMessage = QMessageBox(self)
                    deletionMessage.setWindowTitle(self.string_list_dialog[4])
                    message = self.string_list_dialog[5]
                    message = message.format(id = res[0][0], user = self.current_user)
                    deletionMessage.setText(message)
                    deletionMessage.setWindowModality(Qt.ApplicationModal)
                    deletionMessage.show()

            deletionDialog = QMessageBox(self)
            deletionDialog.setWindowTitle(self.string_list_dialog[3])
            deletionDialog.setText(self.string_list_dialog[2])
            deletionDialog.setWindowModality(Qt.ApplicationModal)
            deletionDialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            yes_button = deletionDialog.button(QMessageBox.Yes)
            no_button = deletionDialog.button(QMessageBox.No)
            yes_button.setText(self.string_list_dialog[0])
            no_button.setText(self.string_list_dialog[1])
            deletionDialog.buttonClicked.connect(lambda btn: on_accept() if btn == yes_button else None)
            deletionDialog.show()
        except Exception as e:
            logger.debug(f"SharedUserStatsModel delete_session_handler error: {e}")

    def stop_button_handler(self):
        try:
            self.dataCollectorHandler.stop_data_collection()
            self.button_toggler(self.stopListening)
            self.update_session_chart_value()
            self.update_summary_charts()
        except Exception as e:
            logger.debug(f"SharedUserStatsModel stop_button_handler error: {e}")

    def comboBox_change_handler(self):
        try:
            current_index = self.sessionComboBox.currentData()
            if (current_index != self.latest_session):
                self.startListening.setEnabled(False)
            else:
                self.startListening.setEnabled(True)
            self.update_session_chart_value()  
            self.update_summary_charts()
        except Exception as e:
            logger.debug(f"SharedUserStatsModel comboBox_change_handler error: {e}")

    def start_button_handler(self):
        try:
            if self.btSerialHandle.socket_none_check():
                return
            self.dataCollectorHandler.start_watch = True
            self.button_toggler(self.startListening)
        except Exception as e:
            logger.debug(f"SharedUserStatsModel start_button_handler error: {e}")

    def new_session_button_handler(self):
        try:
            session_id = self.create_session()
            if session_id:
                self.populate_comboBox()
        except Exception as e:
            logger.debug(f"SharedUserStatsModel new_session_button_handler error: {e}")

    def assing_user(self,user_index,user_name):
        try:
            self.current_user = user_index
            self.dataCollectorHandler.current_user_index = self.current_user
            self.current_user_name = user_name
            self.populate_comboBox()
        except Exception as e:
            logger.debug(f"SharedUserStatsModel assing_user error: {e}")

    def create_session(self):
        try:
            q = f"""insert into session (patient_id, session_date) values (?,datetime(current_timestamp,'localtime')) returning patient_id,id;"""
            res = self.dbHandleClass.execute_single_query(q,[self.current_user])
            if res:
                logger.debug(f"Seção criada para o usuário {res[0][0]}")
                return res[0][1]
            else:
                return False
        except Exception as e:
            logger.debug(f"SharedUserStatsModel create_session error: {e}")

    def get_sessions(self):
        try:
            qSessions = f"select * from session where patient_id = ?;"
            resSessions = self.dbHandleClass.execute_single_query(qSessions,[self.current_user])
            if resSessions:
                return resSessions
        except Exception as e:
            logger.debug(f"SharedUserStatsModel get_sessions error: {e}")

    def populate_comboBox(self):
        try:
            self.sessionComboBox.clear()
            sessions = self.get_sessions()
            if sessions:
                for s in sessions:
                    text = str(s[2])
                    latest_session = s[0]
                    self.assing_latest_session(latest_session)
                    self.sessionComboBox.addItem(text[:len(text)-3],s[0])
                self.sessionComboBox.setCurrentIndex(self.sessionComboBox.count()-1)
        except Exception as e:
            logger.debug(f"SharedUserStatsModel populate_comboBox error: {e}")

    def assing_latest_session(self,latest_session):
        try:
            self.latest_session = latest_session
            self.dataCollectorHandler.current_session_index = latest_session
        except Exception as e:
            logger.debug(f"SharedUserStatsModel assing_latest_session error: {e}")

    def set_dialog_text(self):
        #dialog text
        self.string_list_dialog = [
            QCoreApplication.translate("UserStatsDialogText","Confirmar"),
            QCoreApplication.translate("UserStatsDialogText","Cancelar"),
            QCoreApplication.translate("UserStatsDialogText","Deseja excluir a sessão selecionada?"),
            QCoreApplication.translate("UserStatsDialogText","Aviso"),
            QCoreApplication.translate("UserStatsDialogText","Sucesso"),
            QCoreApplication.translate("UserStatsDialogText","Sessão de id {id}, do usuário {user} removida")
        ]
        

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.delete_charts()
            self.create_charts()
            self.update_session_chart_value()
            self.update_summary_charts()
            self.set_dialog_text()
        return super().changeEvent(event)
        