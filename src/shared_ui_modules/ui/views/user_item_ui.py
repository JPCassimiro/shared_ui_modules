# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_item.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

from shared_ui_modules.ui.model.custom_widgets.rounded_image_label import RoundedImageLabel

class Ui_userItemForm(object):
    def setupUi(self, userItemForm):
        if not userItemForm.objectName():
            userItemForm.setObjectName(u"userItemForm")
        userItemForm.resize(548, 138)
        self.gridLayout = QGridLayout(userItemForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.userItemWidgetContainer = QWidget(userItemForm)
        self.userItemWidgetContainer.setObjectName(u"userItemWidgetContainer")
        self.horizontalLayout_2 = QHBoxLayout(self.userItemWidgetContainer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.imageContainer = QWidget(self.userItemWidgetContainer)
        self.imageContainer.setObjectName(u"imageContainer")
        self.verticalLayout_2 = QVBoxLayout(self.imageContainer)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.itemImageLabel = RoundedImageLabel(self.imageContainer)
        self.itemImageLabel.setObjectName(u"itemImageLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemImageLabel.sizePolicy().hasHeightForWidth())
        self.itemImageLabel.setSizePolicy(sizePolicy)
        self.itemImageLabel.setMaximumSize(QSize(100, 100))
        self.itemImageLabel.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.itemImageLabel)


        self.horizontalLayout_2.addWidget(self.imageContainer)

        self.textContainer = QWidget(self.userItemWidgetContainer)
        self.textContainer.setObjectName(u"textContainer")
        self.verticalLayout = QVBoxLayout(self.textContainer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nameLabel = QLabel(self.textContainer)
        self.nameLabel.setObjectName(u"nameLabel")

        self.verticalLayout.addWidget(self.nameLabel)

        self.functionLabel = QLabel(self.textContainer)
        self.functionLabel.setObjectName(u"functionLabel")

        self.verticalLayout.addWidget(self.functionLabel)


        self.horizontalLayout_2.addWidget(self.textContainer)

        self.buttonsContainer = QWidget(self.userItemWidgetContainer)
        self.buttonsContainer.setObjectName(u"buttonsContainer")
        self.verticalLayout_3 = QVBoxLayout(self.buttonsContainer)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.editButton = QToolButton(self.buttonsContainer)
        self.editButton.setObjectName(u"editButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailMessageNew))
        self.editButton.setIcon(icon)

        self.verticalLayout_3.addWidget(self.editButton)

        self.removeButton = QToolButton(self.buttonsContainer)
        self.removeButton.setObjectName(u"removeButton")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.removeButton.setIcon(icon1)

        self.verticalLayout_3.addWidget(self.removeButton)


        self.horizontalLayout_2.addWidget(self.buttonsContainer)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)

        self.gridLayout.addWidget(self.userItemWidgetContainer, 0, 0, 1, 1)


        self.retranslateUi(userItemForm)

        QMetaObject.connectSlotsByName(userItemForm)
    # setupUi

    def retranslateUi(self, userItemForm):
        userItemForm.setWindowTitle(QCoreApplication.translate("userItemForm", u"Form", None))
        self.itemImageLabel.setText("")
        self.nameLabel.setText(QCoreApplication.translate("userItemForm", u"TextLabel", None))
        self.functionLabel.setText(QCoreApplication.translate("userItemForm", u"TextLabel", None))
        self.editButton.setText(QCoreApplication.translate("userItemForm", u"...", None))
        self.removeButton.setText(QCoreApplication.translate("userItemForm", u"...", None))
    # retranslateUi

