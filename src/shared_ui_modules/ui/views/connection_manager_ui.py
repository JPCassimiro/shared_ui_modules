# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'connection_manager.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

class Ui_loggerForm(object):
    def setupUi(self, loggerForm):
        if not loggerForm.objectName():
            loggerForm.setObjectName(u"loggerForm")
        loggerForm.resize(648, 445)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(loggerForm.sizePolicy().hasHeightForWidth())
        loggerForm.setSizePolicy(sizePolicy)
        loggerForm.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(loggerForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, -1, -1, -1)
        self.windowContainer = QWidget(loggerForm)
        self.windowContainer.setObjectName(u"windowContainer")
        self.gridLayout_2 = QGridLayout(self.windowContainer)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.deviceListContainer = QWidget(self.windowContainer)
        self.deviceListContainer.setObjectName(u"deviceListContainer")
        self.gridLayout_3 = QGridLayout(self.deviceListContainer)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.deviceListWidget = QListWidget(self.deviceListContainer)
        self.deviceListWidget.setObjectName(u"deviceListWidget")
        self.deviceListWidget.setFrameShadow(QFrame.Shadow.Plain)

        self.gridLayout_3.addWidget(self.deviceListWidget, 1, 0, 1, 1)

        self.deviceListButtonContainer = QWidget(self.deviceListContainer)
        self.deviceListButtonContainer.setObjectName(u"deviceListButtonContainer")
        self.horizontalLayout = QHBoxLayout(self.deviceListButtonContainer)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.reloadListButton = QToolButton(self.deviceListButtonContainer)
        self.reloadListButton.setObjectName(u"reloadListButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.reloadListButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.reloadListButton)

        self.pairDeviceButton = QPushButton(self.deviceListButtonContainer)
        self.pairDeviceButton.setObjectName(u"pairDeviceButton")

        self.horizontalLayout.addWidget(self.pairDeviceButton)

        self.pairButtonInstructionLabel = QLabel(self.deviceListButtonContainer)
        self.pairButtonInstructionLabel.setObjectName(u"pairButtonInstructionLabel")

        self.horizontalLayout.addWidget(self.pairButtonInstructionLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_3.addWidget(self.deviceListButtonContainer, 2, 0, 1, 1)

        self.listTitleLabel = QLabel(self.deviceListContainer)
        self.listTitleLabel.setObjectName(u"listTitleLabel")
        font = QFont()
        font.setBold(True)
        self.listTitleLabel.setFont(font)
        self.listTitleLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.listTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.listTitleLabel, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.deviceListContainer, 0, 0, 1, 1)

        self.selectedDeviceContainer = QWidget(self.windowContainer)
        self.selectedDeviceContainer.setObjectName(u"selectedDeviceContainer")
        self.verticalLayout_2 = QVBoxLayout(self.selectedDeviceContainer)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.selectedDeviceTitleLabel = QLabel(self.selectedDeviceContainer)
        self.selectedDeviceTitleLabel.setObjectName(u"selectedDeviceTitleLabel")
        self.selectedDeviceTitleLabel.setFont(font)
        self.selectedDeviceTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.selectedDeviceTitleLabel)

        self.deviceContainerFrame = QFrame(self.selectedDeviceContainer)
        self.deviceContainerFrame.setObjectName(u"deviceContainerFrame")
        self.deviceContainerFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.deviceContainerFrame.setFrameShadow(QFrame.Shadow.Sunken)
        self.deviceContainerFrame.setLineWidth(1)
        self.deviceContainerFrame.setMidLineWidth(0)
        self.gridLayout_4 = QGridLayout(self.deviceContainerFrame)
        self.gridLayout_4.setSpacing(3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(3, 3, 3, 3)
        self.deviceContainer = QWidget(self.deviceContainerFrame)
        self.deviceContainer.setObjectName(u"deviceContainer")
        self.gridLayout_5 = QGridLayout(self.deviceContainer)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_4.addWidget(self.deviceContainer, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.deviceContainerFrame)

        self.unpairDeviceButton = QPushButton(self.selectedDeviceContainer)
        self.unpairDeviceButton.setObjectName(u"unpairDeviceButton")

        self.verticalLayout_2.addWidget(self.unpairDeviceButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(3, 2)

        self.gridLayout_2.addWidget(self.selectedDeviceContainer, 0, 1, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 2)
        self.gridLayout_2.setColumnStretch(1, 1)

        self.gridLayout.addWidget(self.windowContainer, 0, 2, 1, 1)


        self.retranslateUi(loggerForm)

        QMetaObject.connectSlotsByName(loggerForm)
    # setupUi

    def retranslateUi(self, loggerForm):
        loggerForm.setWindowTitle(QCoreApplication.translate("loggerForm", u"Form", None))
#if QT_CONFIG(tooltip)
        self.reloadListButton.setToolTip(QCoreApplication.translate("loggerForm", u"Procurar por dispositivos", u"ConnectionManagerHelper"))
#endif // QT_CONFIG(tooltip)
        self.reloadListButton.setText(QCoreApplication.translate("loggerForm", u"...", None))
        self.pairDeviceButton.setText(QCoreApplication.translate("loggerForm", u"Emparelhar dispositivo", None))
        self.pairButtonInstructionLabel.setText(QCoreApplication.translate("loggerForm", u"Selecione um dispositivo para emparelhar", None))
        self.listTitleLabel.setText(QCoreApplication.translate("loggerForm", u"Lista de dispositivos encontrados", None))
        self.selectedDeviceTitleLabel.setText(QCoreApplication.translate("loggerForm", u"Dispositivo Conectado", None))
        self.unpairDeviceButton.setText(QCoreApplication.translate("loggerForm", u"Desemparelhar dispositivo", None))
    # retranslateUi

