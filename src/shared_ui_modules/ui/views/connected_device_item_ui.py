# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'connected_device_item.ui'
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
    QWidget)

class Ui_selectedDeviceForm(object):
    def setupUi(self, selectedDeviceForm):
        if not selectedDeviceForm.objectName():
            selectedDeviceForm.setObjectName(u"selectedDeviceForm")
        selectedDeviceForm.resize(228, 140)
        self.gridLayout = QGridLayout(selectedDeviceForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.windowContainer = QWidget(selectedDeviceForm)
        self.windowContainer.setObjectName(u"windowContainer")
        self.gridLayout_2 = QGridLayout(self.windowContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comPortLabel = QLabel(self.windowContainer)
        self.comPortLabel.setObjectName(u"comPortLabel")

        self.gridLayout_2.addWidget(self.comPortLabel, 1, 0, 1, 1)

        self.sppCheckLabel = QLabel(self.windowContainer)
        self.sppCheckLabel.setObjectName(u"sppCheckLabel")

        self.gridLayout_2.addWidget(self.sppCheckLabel, 3, 0, 1, 1)

        self.hidCheckLabel = QLabel(self.windowContainer)
        self.hidCheckLabel.setObjectName(u"hidCheckLabel")

        self.gridLayout_2.addWidget(self.hidCheckLabel, 4, 0, 1, 1)

        self.macLabel = QLabel(self.windowContainer)
        self.macLabel.setObjectName(u"macLabel")

        self.gridLayout_2.addWidget(self.macLabel, 2, 0, 1, 1)

        self.deviceNameLabel = QLabel(self.windowContainer)
        self.deviceNameLabel.setObjectName(u"deviceNameLabel")

        self.gridLayout_2.addWidget(self.deviceNameLabel, 0, 0, 1, 1)

        self.deviceIconLabel = QLabel(self.windowContainer)
        self.deviceIconLabel.setObjectName(u"deviceIconLabel")
        self.deviceIconLabel.setMinimumSize(QSize(32, 32))
        self.deviceIconLabel.setMaximumSize(QSize(32, 32))
        self.deviceIconLabel.setText(u"")
        self.deviceIconLabel.setPixmap(QPixmap(u"_internal/resources/icons/joystick.png"))
        self.deviceIconLabel.setScaledContents(True)

        self.gridLayout_2.addWidget(self.deviceIconLabel, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.windowContainer, 0, 0, 1, 1)


        self.retranslateUi(selectedDeviceForm)

        QMetaObject.connectSlotsByName(selectedDeviceForm)
    # setupUi

    def retranslateUi(self, selectedDeviceForm):
        selectedDeviceForm.setWindowTitle(QCoreApplication.translate("selectedDeviceForm", u"Form", None))
        self.comPortLabel.setText(QCoreApplication.translate("selectedDeviceForm", u"TextLabel", None))
        self.sppCheckLabel.setText(QCoreApplication.translate("selectedDeviceForm", u"TextLabel", None))
        self.hidCheckLabel.setText(QCoreApplication.translate("selectedDeviceForm", u"TextLabel", None))
        self.macLabel.setText(QCoreApplication.translate("selectedDeviceForm", u"TextLabel", None))
        self.deviceNameLabel.setText(QCoreApplication.translate("selectedDeviceForm", u"TextLabel", None))
    # retranslateUi

