# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'end_config_modal.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QSizePolicy,
    QTextEdit, QWidget)

class Ui_endConfigModalDialog(object):
    def setupUi(self, endConfigModalDialog):
        if not endConfigModalDialog.objectName():
            endConfigModalDialog.setObjectName(u"endConfigModalDialog")
        endConfigModalDialog.resize(238, 155)
        self.gridLayout = QGridLayout(endConfigModalDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.modalContainer = QWidget(endConfigModalDialog)
        self.modalContainer.setObjectName(u"modalContainer")
        self.gridLayout_2 = QGridLayout(self.modalContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.messageWidgetContainer = QWidget(self.modalContainer)
        self.messageWidgetContainer.setObjectName(u"messageWidgetContainer")
        self.gridLayout_3 = QGridLayout(self.messageWidgetContainer)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.messageField = QTextEdit(self.messageWidgetContainer)
        self.messageField.setObjectName(u"messageField")
        self.messageField.setReadOnly(True)

        self.gridLayout_3.addWidget(self.messageField, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.messageWidgetContainer, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.modalContainer, 0, 0, 1, 1)


        self.retranslateUi(endConfigModalDialog)

        QMetaObject.connectSlotsByName(endConfigModalDialog)
    # setupUi

    def retranslateUi(self, endConfigModalDialog):
        endConfigModalDialog.setWindowTitle(QCoreApplication.translate("endConfigModalDialog", u"Dialog", None))
    # retranslateUi

