from shared_ui_modules.ui.views.patient_widget_ui import Ui_patientWindowContainer
from shared_ui_modules.modules.log_class import logger
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap


class SharedPatientWidgetModel(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_patientWindowContainer()
        self.ui.setupUi(self)
        
        self.info_dict = None    
    
        #components
        self.patientImage = self.ui.patientImage
        self.patientName = self.ui.patientName
        self.patientInfo = self.ui.patientInfo
        
    def update_fields(self):
        self.patientInfo.setText(self.info_dict["details"])
        self.patientName.setText(self.info_dict["name"])
        self.set_image(self.info_dict["image_path"])
        
    def set_image(self,img_path):
        try:
            img = QPixmap()
            if img.load(img_path):
                self.patientImage.setPixmap(img)
                self.patientImage.setScaledContents(True)
            else:
                logger.error(f"Erro ao cerregar imagem no caminho: {img_path}")
        except Exception as e:
            logger.error(f"Erro ao atribuir uma imagem no widget do paciente: {e}")