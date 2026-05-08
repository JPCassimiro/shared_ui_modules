# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_modal.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QPlainTextEdit,
    QSizePolicy, QWidget)

class Ui_logDialogForm(object):
    def setupUi(self, logDialogForm):
        if not logDialogForm.objectName():
            logDialogForm.setObjectName(u"logDialogForm")
        logDialogForm.resize(292, 228)
        self.gridLayout = QGridLayout(logDialogForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.logEditContainer = QWidget(logDialogForm)
        self.logEditContainer.setObjectName(u"logEditContainer")
        self.gridLayout_2 = QGridLayout(self.logEditContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.logTextEdit = QPlainTextEdit(self.logEditContainer)
        self.logTextEdit.setObjectName(u"logTextEdit")
        self.logTextEdit.setReadOnly(True)

        self.gridLayout_2.addWidget(self.logTextEdit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.logEditContainer, 0, 0, 1, 1)


        self.retranslateUi(logDialogForm)

        QMetaObject.connectSlotsByName(logDialogForm)
    # setupUi

    def retranslateUi(self, logDialogForm):
        logDialogForm.setWindowTitle(QCoreApplication.translate("logDialogForm", u"Dialog", None))
    # retranslateUi

