# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_helper_modal.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_appHelpDialog(object):
    def setupUi(self, appHelpDialog):
        if not appHelpDialog.objectName():
            appHelpDialog.setObjectName(u"appHelpDialog")
        appHelpDialog.resize(269, 118)
        appHelpDialog.setMaximumSize(QSize(300, 312))
        self.gridLayout = QGridLayout(appHelpDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.appHelpContainer = QWidget(appHelpDialog)
        self.appHelpContainer.setObjectName(u"appHelpContainer")
        self.gridLayout_2 = QGridLayout(self.appHelpContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(15, 15, 15, 15)
        self.linkContainer = QWidget(self.appHelpContainer)
        self.linkContainer.setObjectName(u"linkContainer")
        self.gridLayout_4 = QGridLayout(self.linkContainer)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.utfprLogoContainer = QWidget(self.linkContainer)
        self.utfprLogoContainer.setObjectName(u"utfprLogoContainer")
        self.utfprLogoContainer.setMaximumSize(QSize(80, 30))
        self.verticalLayout = QVBoxLayout(self.utfprLogoContainer)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.utfprLogoLabel = QLabel(self.utfprLogoContainer)
        self.utfprLogoLabel.setObjectName(u"utfprLogoLabel")
        self.utfprLogoLabel.setPixmap(QPixmap(u"_internal/resources/icons/utfprLogo.png"))
        self.utfprLogoLabel.setScaledContents(True)

        self.verticalLayout.addWidget(self.utfprLogoLabel)


        self.gridLayout_4.addWidget(self.utfprLogoContainer, 0, 1, 1, 1)

        self.manualLinkLabel = QLabel(self.linkContainer)
        self.manualLinkLabel.setObjectName(u"manualLinkLabel")
        self.manualLinkLabel.setTextFormat(Qt.TextFormat.RichText)
        self.manualLinkLabel.setOpenExternalLinks(False)

        self.gridLayout_4.addWidget(self.manualLinkLabel, 0, 0, 1, 1)

        self.githubLinkLabel = QLabel(self.linkContainer)
        self.githubLinkLabel.setObjectName(u"githubLinkLabel")
        self.githubLinkLabel.setOpenExternalLinks(True)

        self.gridLayout_4.addWidget(self.githubLinkLabel, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.linkContainer, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.appHelpContainer, 1, 1, 1, 1)


        self.retranslateUi(appHelpDialog)

        QMetaObject.connectSlotsByName(appHelpDialog)
    # setupUi

    def retranslateUi(self, appHelpDialog):
        appHelpDialog.setWindowTitle(QCoreApplication.translate("appHelpDialog", u"Dialog", None))
        self.utfprLogoLabel.setText("")
        self.manualLinkLabel.setText(QCoreApplication.translate("appHelpDialog", u"<a href=\"file:///manual/manual.html\">Manual de usu\u00e1rio<a/>", None))
        self.githubLinkLabel.setText(QCoreApplication.translate("appHelpDialog", u"<a href=\"https://github.com/JPCassimiro/JHMR\">Reposit\u00f3rio no Github</a>", None))
    # retranslateUi

