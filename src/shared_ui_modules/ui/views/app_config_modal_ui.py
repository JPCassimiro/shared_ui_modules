# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_config_modal.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QLabel, QSizePolicy, QSpacerItem, QWidget)

class Ui_AppConfigDialog(object):
    def setupUi(self, AppConfigDialog):
        if not AppConfigDialog.objectName():
            AppConfigDialog.setObjectName(u"AppConfigDialog")
        AppConfigDialog.resize(400, 300)
        self.gridLayout = QGridLayout(AppConfigDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.AppConfigContainer = QWidget(AppConfigDialog)
        self.AppConfigContainer.setObjectName(u"AppConfigContainer")
        self.gridLayout_2 = QGridLayout(self.AppConfigContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.languageSelectoLabel = QLabel(self.AppConfigContainer)
        self.languageSelectoLabel.setObjectName(u"languageSelectoLabel")

        self.gridLayout_2.addWidget(self.languageSelectoLabel, 0, 0, 1, 1)

        self.languageSelectionComboBox = QComboBox(self.AppConfigContainer)
        self.languageSelectionComboBox.setObjectName(u"languageSelectionComboBox")

        self.gridLayout_2.addWidget(self.languageSelectionComboBox, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.AppConfigContainer, 0, 0, 1, 1)


        self.retranslateUi(AppConfigDialog)

        QMetaObject.connectSlotsByName(AppConfigDialog)
    # setupUi

    def retranslateUi(self, AppConfigDialog):
        AppConfigDialog.setWindowTitle(QCoreApplication.translate("AppConfigDialog", u"Dialog", None))
        self.languageSelectoLabel.setText(QCoreApplication.translate("AppConfigDialog", u"Lingua", None))
    # retranslateUi

