# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QLineEdit, QSizePolicy,
    QToolButton, QWidget)

class Ui_registerDialog(object):
    def setupUi(self, registerDialog):
        if not registerDialog.objectName():
            registerDialog.setObjectName(u"registerDialog")
        registerDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        registerDialog.resize(393, 208)
        registerDialog.setModal(True)
        self.gridLayout = QGridLayout(registerDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.registerWidgetContainer = QWidget(registerDialog)
        self.registerWidgetContainer.setObjectName(u"registerWidgetContainer")
        self.gridLayout_2 = QGridLayout(self.registerWidgetContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.nameLabel = QLabel(self.registerWidgetContainer)
        self.nameLabel.setObjectName(u"nameLabel")

        self.gridLayout_2.addWidget(self.nameLabel, 0, 1, 1, 1)

        self.imageSelectButton = QToolButton(self.registerWidgetContainer)
        self.imageSelectButton.setObjectName(u"imageSelectButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.imageSelectButton.setIcon(icon)

        self.gridLayout_2.addWidget(self.imageSelectButton, 5, 2, 1, 1)

        self.nameEdit = QLineEdit(self.registerWidgetContainer)
        self.nameEdit.setObjectName(u"nameEdit")
        self.nameEdit.setMaxLength(32)

        self.gridLayout_2.addWidget(self.nameEdit, 1, 1, 1, 1)

        self.imageLineEdit = QLineEdit(self.registerWidgetContainer)
        self.imageLineEdit.setObjectName(u"imageLineEdit")
        self.imageLineEdit.setReadOnly(True)

        self.gridLayout_2.addWidget(self.imageLineEdit, 5, 1, 1, 1)

        self.imagePreview = QLabel(self.registerWidgetContainer)
        self.imagePreview.setObjectName(u"imagePreview")

        self.gridLayout_2.addWidget(self.imagePreview, 4, 1, 1, 1)

        self.descriptionLabel = QLabel(self.registerWidgetContainer)
        self.descriptionLabel.setObjectName(u"descriptionLabel")

        self.gridLayout_2.addWidget(self.descriptionLabel, 2, 1, 1, 1)

        self.descriptionEdit = QLineEdit(self.registerWidgetContainer)
        self.descriptionEdit.setObjectName(u"descriptionEdit")
        self.descriptionEdit.setMaxLength(32)

        self.gridLayout_2.addWidget(self.descriptionEdit, 3, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(self.registerWidgetContainer)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_2.addWidget(self.buttonBox, 6, 1, 1, 1)


        self.gridLayout.addWidget(self.registerWidgetContainer, 0, 0, 1, 1)


        self.retranslateUi(registerDialog)
        self.buttonBox.accepted.connect(registerDialog.accept)
        self.buttonBox.rejected.connect(registerDialog.reject)

        QMetaObject.connectSlotsByName(registerDialog)
    # setupUi

    def retranslateUi(self, registerDialog):
        registerDialog.setWindowTitle(QCoreApplication.translate("registerDialog", u"Dialog", None))
        self.nameLabel.setText(QCoreApplication.translate("registerDialog", u"Nome (obrigat\u00f3rio)", None))
        self.imageSelectButton.setText(QCoreApplication.translate("registerDialog", u"...", None))
        self.imageLineEdit.setPlaceholderText(QCoreApplication.translate("registerDialog", u"Selecione uma imagem", None))
        self.imagePreview.setText(QCoreApplication.translate("registerDialog", u"Imagem de perfil", None))
        self.descriptionLabel.setText(QCoreApplication.translate("registerDialog", u"Descri\u00e7\u00e3o (obrigat\u00f3rio)", None))
    # retranslateUi

