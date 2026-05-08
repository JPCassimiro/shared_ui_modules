# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_profile_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_gameProfileWidgetForm(object):
    def setupUi(self, gameProfileWidgetForm):
        if not gameProfileWidgetForm.objectName():
            gameProfileWidgetForm.setObjectName(u"gameProfileWidgetForm")
        gameProfileWidgetForm.resize(792, 507)
        self.gridLayout = QGridLayout(gameProfileWidgetForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gameProfileContainer = QWidget(gameProfileWidgetForm)
        self.gameProfileContainer.setObjectName(u"gameProfileContainer")
        self.horizontalLayout = QHBoxLayout(self.gameProfileContainer)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.gameProfileListContainer = QWidget(self.gameProfileContainer)
        self.gameProfileListContainer.setObjectName(u"gameProfileListContainer")
        self.verticalLayout = QVBoxLayout(self.gameProfileListContainer)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gameProfileList = QListWidget(self.gameProfileListContainer)
        self.gameProfileList.setObjectName(u"gameProfileList")
        self.gameProfileList.setResizeMode(QListView.ResizeMode.Adjust)
        self.gameProfileList.setSpacing(4)
        self.gameProfileList.setViewMode(QListView.ViewMode.ListMode)
        self.gameProfileList.setUniformItemSizes(False)

        self.verticalLayout.addWidget(self.gameProfileList)

        self.gameProfileLineEdit = QLineEdit(self.gameProfileListContainer)
        self.gameProfileLineEdit.setObjectName(u"gameProfileLineEdit")
        self.gameProfileLineEdit.setMaxLength(32)

        self.verticalLayout.addWidget(self.gameProfileLineEdit)

        self.newGameProfileButton = QPushButton(self.gameProfileListContainer)
        self.newGameProfileButton.setObjectName(u"newGameProfileButton")

        self.verticalLayout.addWidget(self.newGameProfileButton)

        self.deleteGameProfileButton = QPushButton(self.gameProfileListContainer)
        self.deleteGameProfileButton.setObjectName(u"deleteGameProfileButton")

        self.verticalLayout.addWidget(self.deleteGameProfileButton)


        self.horizontalLayout.addWidget(self.gameProfileListContainer)

        self.controlContainer = QWidget(self.gameProfileContainer)
        self.controlContainer.setObjectName(u"controlContainer")
        self.horizontalLayout_2 = QHBoxLayout(self.controlContainer)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.cardListWidget = QListWidget(self.controlContainer)
        self.cardListWidget.setObjectName(u"cardListWidget")
        self.cardListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cardListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cardListWidget.setFlow(QListView.Flow.LeftToRight)
        self.cardListWidget.setResizeMode(QListView.ResizeMode.Adjust)
        self.cardListWidget.setSpacing(5)
        self.cardListWidget.setViewMode(QListView.ViewMode.IconMode)
        self.cardListWidget.setUniformItemSizes(False)

        self.horizontalLayout_2.addWidget(self.cardListWidget)

        self.cardButtonContainer = QWidget(self.controlContainer)
        self.cardButtonContainer.setObjectName(u"cardButtonContainer")
        self.verticalLayout_2 = QVBoxLayout(self.cardButtonContainer)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.addNewCardButton = QPushButton(self.cardButtonContainer)
        self.addNewCardButton.setObjectName(u"addNewCardButton")
        self.addNewCardButton.setAutoDefault(False)
        self.addNewCardButton.setFlat(False)

        self.verticalLayout_2.addWidget(self.addNewCardButton)

        self.deleteCardButton = QPushButton(self.cardButtonContainer)
        self.deleteCardButton.setObjectName(u"deleteCardButton")

        self.verticalLayout_2.addWidget(self.deleteCardButton)

        self.applySelectedCardButton = QPushButton(self.cardButtonContainer)
        self.applySelectedCardButton.setObjectName(u"applySelectedCardButton")

        self.verticalLayout_2.addWidget(self.applySelectedCardButton)

        self.applyAllCardsButton = QPushButton(self.cardButtonContainer)
        self.applyAllCardsButton.setObjectName(u"applyAllCardsButton")

        self.verticalLayout_2.addWidget(self.applyAllCardsButton)

        self.sendToConfigScreenButton = QPushButton(self.cardButtonContainer)
        self.sendToConfigScreenButton.setObjectName(u"sendToConfigScreenButton")

        self.verticalLayout_2.addWidget(self.sendToConfigScreenButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addWidget(self.cardButtonContainer)

        self.horizontalLayout_2.setStretch(0, 2)

        self.horizontalLayout.addWidget(self.controlContainer)

        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 14)

        self.gridLayout.addWidget(self.gameProfileContainer, 0, 0, 1, 1)


        self.retranslateUi(gameProfileWidgetForm)

        self.addNewCardButton.setDefault(False)


        QMetaObject.connectSlotsByName(gameProfileWidgetForm)
    # setupUi

    def retranslateUi(self, gameProfileWidgetForm):
        gameProfileWidgetForm.setWindowTitle(QCoreApplication.translate("gameProfileWidgetForm", u"Form", None))
        self.gameProfileLineEdit.setText("")
        self.gameProfileLineEdit.setPlaceholderText(QCoreApplication.translate("gameProfileWidgetForm", u"Digite o nome do novo perfil", None))
        self.newGameProfileButton.setText(QCoreApplication.translate("gameProfileWidgetForm", u"Criar novo perfil", None))
        self.deleteGameProfileButton.setText(QCoreApplication.translate("gameProfileWidgetForm", u"Remover perfil", None))
#if QT_CONFIG(tooltip)
        self.addNewCardButton.setToolTip(QCoreApplication.translate("gameProfileWidgetForm", u"Adicionar ultima configura\u00e7\u00e3o realizada na tela de configura\u00e7\u00f5es ao perfil", u"gameProfileHelper"))
#endif // QT_CONFIG(tooltip)
        self.addNewCardButton.setText(QCoreApplication.translate("gameProfileWidgetForm", u"Adicionar nova\n"
"configura\u00e7\u00e3o", None))
#if QT_CONFIG(tooltip)
        self.deleteCardButton.setToolTip(QCoreApplication.translate("gameProfileWidgetForm", u"Remover configura\u00e7\u00e3o selecionada", u"gameProfileHelper"))
#endif // QT_CONFIG(tooltip)
        self.deleteCardButton.setText(QCoreApplication.translate("gameProfileWidgetForm", u"Remover\n"
"configura\u00e7\u00e3o", None))
#if QT_CONFIG(tooltip)
        self.applySelectedCardButton.setToolTip(QCoreApplication.translate("gameProfileWidgetForm", u"Aplicar confgura\u00e7\u00e3o selecionada ao joystick", u"gameProfileHelper"))
#endif // QT_CONFIG(tooltip)
        self.applySelectedCardButton.setText(QCoreApplication.translate("gameProfileWidgetForm", u"Aplicar configura\u00e7\u00e3o\n"
"selecionada", None))
#if QT_CONFIG(tooltip)
        self.applyAllCardsButton.setToolTip(QCoreApplication.translate("gameProfileWidgetForm", u"Aplicar todas as configura\u00e7\u00f5es do perfil ao joystick", u"gameProfileHelper"))
#endif // QT_CONFIG(tooltip)
        self.applyAllCardsButton.setText(QCoreApplication.translate("gameProfileWidgetForm", u"Aplicar todas\n"
"as configura\u00e7\u00f5es", None))
#if QT_CONFIG(tooltip)
        self.sendToConfigScreenButton.setToolTip(QCoreApplication.translate("gameProfileWidgetForm", u"Enviar congura\u00e7\u00e3o selecionada para tela de configura\u00e7\u00f5es", u"gameProfileHelper"))
#endif // QT_CONFIG(tooltip)
        self.sendToConfigScreenButton.setText(QCoreApplication.translate("gameProfileWidgetForm", u"Enviar para\n"
"tela de configura\u00e7\u00e3o", None))
    # retranslateUi

