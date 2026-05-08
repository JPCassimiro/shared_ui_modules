# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'title_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

from shared_ui_modules.ui.model.custom_widgets.rounded_image_label import RoundedImageLabel

class Ui_titleWindowContainer(object):
    def setupUi(self, titleWindowContainer):
        if not titleWindowContainer.objectName():
            titleWindowContainer.setObjectName(u"titleWindowContainer")
        titleWindowContainer.resize(696, 96)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(titleWindowContainer.sizePolicy().hasHeightForWidth())
        titleWindowContainer.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(titleWindowContainer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.therapistContainer = QWidget(titleWindowContainer)
        self.therapistContainer.setObjectName(u"therapistContainer")
        self.gridLayout_4 = QGridLayout(self.therapistContainer)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.terapistInfoContainer = QWidget(self.therapistContainer)
        self.terapistInfoContainer.setObjectName(u"terapistInfoContainer")
        self.verticalLayout = QVBoxLayout(self.terapistInfoContainer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.therapistName = QLabel(self.terapistInfoContainer)
        self.therapistName.setObjectName(u"therapistName")

        self.verticalLayout.addWidget(self.therapistName)

        self.therapistRole = QLabel(self.terapistInfoContainer)
        self.therapistRole.setObjectName(u"therapistRole")

        self.verticalLayout.addWidget(self.therapistRole)


        self.gridLayout_4.addWidget(self.terapistInfoContainer, 0, 0, 1, 1)

        self.terapistImageContainer = QWidget(self.therapistContainer)
        self.terapistImageContainer.setObjectName(u"terapistImageContainer")
        self.horizontalLayout = QHBoxLayout(self.terapistImageContainer)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.therapistImage = RoundedImageLabel(self.terapistImageContainer)
        self.therapistImage.setObjectName(u"therapistImage")
        self.therapistImage.setMaximumSize(QSize(60, 60))
        self.therapistImage.setPixmap(QPixmap(u"_internal/resources/imgs/placeholder_profile.png"))
        self.therapistImage.setScaledContents(True)

        self.horizontalLayout.addWidget(self.therapistImage)


        self.gridLayout_4.addWidget(self.terapistImageContainer, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.therapistContainer, 0, 1, 1, 1)

        self.softwareTitleContainer = QWidget(titleWindowContainer)
        self.softwareTitleContainer.setObjectName(u"softwareTitleContainer")
        self.gridLayout_3 = QGridLayout(self.softwareTitleContainer)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.softwateTitle = QLabel(self.softwareTitleContainer)
        self.softwateTitle.setObjectName(u"softwateTitle")
        font = QFont()
        font.setFamilies([u"Franklin Gothic"])
        font.setPointSize(22)
        font.setBold(False)
        self.softwateTitle.setFont(font)
        self.softwateTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.softwateTitle, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.softwareTitleContainer, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 2)

        self.retranslateUi(titleWindowContainer)

        QMetaObject.connectSlotsByName(titleWindowContainer)
    # setupUi

    def retranslateUi(self, titleWindowContainer):
        titleWindowContainer.setWindowTitle(QCoreApplication.translate("titleWindowContainer", u"Form", None))
        self.therapistName.setText(QCoreApplication.translate("titleWindowContainer", u"TherapistName", None))
        self.therapistRole.setText(QCoreApplication.translate("titleWindowContainer", u"TherapistFuntion", None))
        self.therapistImage.setText("")
        self.softwateTitle.setText(QCoreApplication.translate("titleWindowContainer", u"Joystick for hand motor rehabilitation", None))
    # retranslateUi

