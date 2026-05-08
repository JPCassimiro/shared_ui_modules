# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'listed_device_item.ui'
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

class Ui_listedDeviceForm(object):
    def setupUi(self, listedDeviceForm):
        if not listedDeviceForm.objectName():
            listedDeviceForm.setObjectName(u"listedDeviceForm")
        listedDeviceForm.resize(498, 94)
        self.gridLayout_2 = QGridLayout(listedDeviceForm)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.listedDeviceWindowContainer = QWidget(listedDeviceForm)
        self.listedDeviceWindowContainer.setObjectName(u"listedDeviceWindowContainer")
        self.gridLayout = QGridLayout(self.listedDeviceWindowContainer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listedDeviceIconLabel = QLabel(self.listedDeviceWindowContainer)
        self.listedDeviceIconLabel.setObjectName(u"listedDeviceIconLabel")

        self.gridLayout.addWidget(self.listedDeviceIconLabel, 0, 1, 1, 1)

        self.listedDeviceNameLabel = QLabel(self.listedDeviceWindowContainer)
        self.listedDeviceNameLabel.setObjectName(u"listedDeviceNameLabel")

        self.gridLayout.addWidget(self.listedDeviceNameLabel, 0, 0, 1, 1)

        self.listedDeviceAddressLabel = QLabel(self.listedDeviceWindowContainer)
        self.listedDeviceAddressLabel.setObjectName(u"listedDeviceAddressLabel")

        self.gridLayout.addWidget(self.listedDeviceAddressLabel, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.listedDeviceWindowContainer, 0, 0, 1, 1)


        self.retranslateUi(listedDeviceForm)

        QMetaObject.connectSlotsByName(listedDeviceForm)
    # setupUi

    def retranslateUi(self, listedDeviceForm):
        listedDeviceForm.setWindowTitle(QCoreApplication.translate("listedDeviceForm", u"Form", None))
        self.listedDeviceIconLabel.setText(QCoreApplication.translate("listedDeviceForm", u"TextLabel", None))
        self.listedDeviceNameLabel.setText(QCoreApplication.translate("listedDeviceForm", u"Dispositivo", None))
        self.listedDeviceAddressLabel.setText(QCoreApplication.translate("listedDeviceForm", u"deviceAddr", None))
    # retranslateUi

