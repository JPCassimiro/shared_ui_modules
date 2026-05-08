from shared_ui_modules.ui.views.title_widget_ui import Ui_titleWindowContainer
from shared_ui_modules.modules.log_class import logger
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap

class SharedTitleWidgetModel(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_titleWindowContainer()
        self.ui.setupUi(self)
        
        self.info_dict = None    
        
        self.title_string = None        
        
        #get elements
        self.therapistImage = self.ui.therapistImage
        self.therapistRole = self.ui.therapistRole
        self.therapistName = self.ui.therapistName
        self.softwareTitle = self.ui.softwateTitle

    def get_title_string(self):
        return

    def initiate_module(self):
        self.title_string = self.get_title_string()
        if self.title_string:
            self.softwareTitle.setText(self.title_string)
    
    def update_fields(self):
        self.therapistName.setText(self.info_dict["name"])
        self.therapistRole.setText(self.info_dict["details"])
        self.set_image(self.info_dict["image_path"])
        
    def set_image(self,img_path):
        try:
            img = QPixmap()
            if img.load(img_path):
                self.therapistImage.setPixmap(img)
                self.therapistImage.setScaledContents(True)
            else:
                logger.error(f"Erro ao cerregar imagem no caminho: {img_path}")
        except Exception as e:
            logger.error(f"Erro ao atribuir uma imagem no widget do paciente: {e}")