# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'patient_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

from shared_ui_modules.ui.model.custom_widgets.rounded_image_label import RoundedImageLabel

class Ui_patientWindowContainer(object):
    def setupUi(self, patientWindowContainer):
        if not patientWindowContainer.objectName():
            patientWindowContainer.setObjectName(u"patientWindowContainer")
        patientWindowContainer.resize(661, 90)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(patientWindowContainer.sizePolicy().hasHeightForWidth())
        patientWindowContainer.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(patientWindowContainer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.patientInfoContainer = QWidget(patientWindowContainer)
        self.patientInfoContainer.setObjectName(u"patientInfoContainer")
        self.verticalLayout = QVBoxLayout(self.patientInfoContainer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.patientName = QLabel(self.patientInfoContainer)
        self.patientName.setObjectName(u"patientName")

        self.verticalLayout.addWidget(self.patientName)

        self.patientInfo = QLabel(self.patientInfoContainer)
        self.patientInfo.setObjectName(u"patientInfo")

        self.verticalLayout.addWidget(self.patientInfo)


        self.gridLayout.addWidget(self.patientInfoContainer, 0, 1, 1, 1)

        self.patientImageContainer = QWidget(patientWindowContainer)
        self.patientImageContainer.setObjectName(u"patientImageContainer")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.patientImageContainer.sizePolicy().hasHeightForWidth())
        self.patientImageContainer.setSizePolicy(sizePolicy1)
        self.gridLayout_2 = QGridLayout(self.patientImageContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.patientImage = RoundedImageLabel(self.patientImageContainer)
        self.patientImage.setObjectName(u"patientImage")
        self.patientImage.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.patientImage.sizePolicy().hasHeightForWidth())
        self.patientImage.setSizePolicy(sizePolicy2)
        self.patientImage.setMinimumSize(QSize(0, 0))
        self.patientImage.setMaximumSize(QSize(60, 60))
        self.patientImage.setTextFormat(Qt.TextFormat.RichText)
        self.patientImage.setPixmap(QPixmap(u"_internal/resources/imgs/placeholder_profile.png"))
        self.patientImage.setScaledContents(True)

        self.gridLayout_2.addWidget(self.patientImage, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.patientImageContainer, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(1, 8)

        self.retranslateUi(patientWindowContainer)

        QMetaObject.connectSlotsByName(patientWindowContainer)
    # setupUi

    def retranslateUi(self, patientWindowContainer):
        patientWindowContainer.setWindowTitle(QCoreApplication.translate("patientWindowContainer", u"Form", None))
        self.patientName.setText(QCoreApplication.translate("patientWindowContainer", u"PatientName", None))
        self.patientInfo.setText(QCoreApplication.translate("patientWindowContainer", u"PatientInfo", None))
        self.patientImage.setText("")
    # retranslateUi

