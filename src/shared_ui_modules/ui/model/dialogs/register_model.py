from shared_ui_modules.ui.views.register_dialog_ui import Ui_registerDialog
from shared_ui_modules.modules.log_class import logger

from PySide6.QtWidgets import QDialog, QFileDialog, QDialogButtonBox
from PySide6.QtCore import Qt, QCoreApplication, QEvent


infoDictBase = {
    "name": None,
    "details": None,
    "image_path": "_internal/resources/imgs/placeholder_profile.png"
}

class RegisterModel(QDialog):
    def __init__(self):
        super().__init__()
        
        #translatable text
        self.string_list_components = [
            QCoreApplication.translate("RegisterDialogText", "Cancelar")
        ]

        #ui setup
        self.ui = Ui_registerDialog()
        self.ui.setupUi(self)

        self.infoDict = infoDictBase.copy()
        
        self.setWindowModality(Qt.ApplicationModal)
        
        self.current_mode = 0 #0 = create, 1 = update
        self.current_table = ""
        
        #get ui elements
        self.nameEdit = self.ui.nameEdit
        self.imageLineEdit = self.ui.imageLineEdit
        self.descriptionEdit = self.ui.descriptionEdit
        self.imageSelectButton = self.ui.imageSelectButton


        #connections
        self.imageSelectButton.clicked.connect(self.select_image_button_handler)
        self.nameEdit.textChanged.connect(self.name_changed_handler)
        self.descriptionEdit.textChanged.connect(self.description_changed_handler)
        
        # self.finished.connect(self.dialog_finish_handler)

        self.set_ui_text()

    def set_ui_text(self):
        self.setWindowTitle(QCoreApplication.translate("RegisterDialogText", "Cadastro"))

        # #edit ok and cancel button names
        # self.ui.buttonBox.button(QDialogButtonBox.Ok).setText(QCoreApplication.translate("RegisterDialogText", "Confirmar"))
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setText(self.string_list_components[0])

    def text_normalization(self):
        try:
            if self.infoDict["name"] != None and self.infoDict["details"] != None:
                name = self.infoDict["name"].strip()
                details = self.infoDict["details"].strip()
                self.infoDict.update({"name":name,"details":details})
        except Exception as e:
            logger.error(f"RegisterModel text_normalization error: {e}")
            raise

    def name_changed_handler(self, text):
        self.infoDict.update({"name": text})
        
    def description_changed_handler(self, text):
        self.infoDict.update({"details": text})
        
    def select_image_button_handler(self):
        try:
            self.image_selector()
        except Exception as e:
            logger.error(f"RegisterModel select_image_button_handler error: {e}")

    def image_selector(self):
        try:
            fileName = QFileDialog.getOpenFileName(self, "Open Image", "./", "Image Files (*.png *.jpg *.bmp)")

            if not fileName:
                raise Exception("null image filename")

            if fileName:
                self.imageLineEdit.setText(f"{fileName[0]}")
                self.infoDict.update({"image_path": fileName[0]})
        except Exception as e:
            logger.error(f"RegisterModel select_image_handler error: {e}")
            raise
        
    def reset_values(self):
        self.imageLineEdit.clear()
        self.nameEdit.clear()
        self.descriptionEdit.clear()
        self.infoDict = infoDictBase.copy()
        
    def complete_fields(self):
        self.nameEdit.setText(self.infoDict["name"])
        self.descriptionEdit.setText(self.infoDict["details"])
        self.imageLineEdit.setText(self.infoDict["image_path"])

    def dialog_finish_handler(self):
        try:
            self.text_normalization()
        except Exception as e:
            logger.error(f"RegisterModel select_image_handler error: {e}")

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.string_list_components = [
                QCoreApplication.translate("RegisterDialogText", "Cancelar")
            ]
            self.set_ui_text()
        return super().changeEvent(event)
        