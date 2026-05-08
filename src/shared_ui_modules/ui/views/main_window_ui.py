# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
    QLabel, QLayout, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTabWidget, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1000, 700))
        font = QFont()
        font.setFamilies([u"Lato"])
        MainWindow.setFont(font)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.MainScreenContainer = QWidget(self.centralwidget)
        self.MainScreenContainer.setObjectName(u"MainScreenContainer")
        self.verticalLayout = QVBoxLayout(self.MainScreenContainer)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.titleWidgetContainer = QWidget(self.MainScreenContainer)
        self.titleWidgetContainer.setObjectName(u"titleWidgetContainer")
        self.verticalLayout_4 = QVBoxLayout(self.titleWidgetContainer)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 3)
        self.titleWidget = QWidget(self.titleWidgetContainer)
        self.titleWidget.setObjectName(u"titleWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.titleWidget.sizePolicy().hasHeightForWidth())
        self.titleWidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.titleWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_4.addWidget(self.titleWidget)


        self.verticalLayout.addWidget(self.titleWidgetContainer)

        self.workplaceContainer = QWidget(self.MainScreenContainer)
        self.workplaceContainer.setObjectName(u"workplaceContainer")
        self.gridLayout_3 = QGridLayout(self.workplaceContainer)
        self.gridLayout_3.setSpacing(1)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(3, 3, 3, 3)
        self.stackedWidgetContainer = QWidget(self.workplaceContainer)
        self.stackedWidgetContainer.setObjectName(u"stackedWidgetContainer")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stackedWidgetContainer.sizePolicy().hasHeightForWidth())
        self.stackedWidgetContainer.setSizePolicy(sizePolicy2)
        self.stackedWidgetContainer.setSizeIncrement(QSize(0, 0))
        self.gridLayout_2 = QGridLayout(self.stackedWidgetContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.stackedWidget = QStackedWidget(self.stackedWidgetContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMidLineWidth(5)
        self.widget_2 = QWidget()
        self.widget_2.setObjectName(u"widget_2")
        self.stackedWidget.addWidget(self.widget_2)
        self.widget_3 = QWidget()
        self.widget_3.setObjectName(u"widget_3")
        self.stackedWidget.addWidget(self.widget_3)

        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.stackedWidgetContainer, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.workplaceContainer)

        self.patientWidgetContainer = QWidget(self.MainScreenContainer)
        self.patientWidgetContainer.setObjectName(u"patientWidgetContainer")
        self.verticalLayout_3 = QVBoxLayout(self.patientWidgetContainer)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(9, 2, -1, 1)
        self.patientWidget = QWidget(self.patientWidgetContainer)
        self.patientWidget.setObjectName(u"patientWidget")
        sizePolicy1.setHeightForWidth(self.patientWidget.sizePolicy().hasHeightForWidth())
        self.patientWidget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.patientWidget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 2, 1, 0)

        self.verticalLayout_3.addWidget(self.patientWidget)


        self.verticalLayout.addWidget(self.patientWidgetContainer)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 20)
        self.verticalLayout.setStretch(2, 1)

        self.gridLayout.addWidget(self.MainScreenContainer, 0, 1, 1, 1)

        self.sideMenu_2 = QWidget(self.centralwidget)
        self.sideMenu_2.setObjectName(u"sideMenu_2")
        self.sideMenu = QVBoxLayout(self.sideMenu_2)
        self.sideMenu.setObjectName(u"sideMenu")
        self.sideMenu.setContentsMargins(0, 5, 5, 0)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.sideMenu.addItem(self.verticalSpacer_2)

        self.logoContainer = QWidget(self.sideMenu_2)
        self.logoContainer.setObjectName(u"logoContainer")
        self.horizontalLayout_3 = QHBoxLayout(self.logoContainer)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.logoLabel = QLabel(self.logoContainer)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setText(u"JHMR")
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.logoLabel)


        self.sideMenu.addWidget(self.logoContainer)

        self.connectionMenuButton = QPushButton(self.sideMenu_2)
        self.connectionMenuButton.setObjectName(u"connectionMenuButton")
        font1 = QFont()
        font1.setFamilies([u"Lato"])
        font1.setPointSize(11)
        self.connectionMenuButton.setFont(font1)
        self.connectionMenuButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.connectionMenuButton.setAutoFillBackground(False)
        self.connectionMenuButton.setIconSize(QSize(32, 32))

        self.sideMenu.addWidget(self.connectionMenuButton, 0, Qt.AlignmentFlag.AlignLeft)

        self.calibrationButton = QPushButton(self.sideMenu_2)
        self.calibrationButton.setObjectName(u"calibrationButton")

        self.sideMenu.addWidget(self.calibrationButton)

        self.configButton = QPushButton(self.sideMenu_2)
        self.configButton.setObjectName(u"configButton")

        self.sideMenu.addWidget(self.configButton)

        self.gameProfileButton = QPushButton(self.sideMenu_2)
        self.gameProfileButton.setObjectName(u"gameProfileButton")

        self.sideMenu.addWidget(self.gameProfileButton)

        self.userActionsButton = QPushButton(self.sideMenu_2)
        self.userActionsButton.setObjectName(u"userActionsButton")

        self.sideMenu.addWidget(self.userActionsButton)

        self.statsButton = QPushButton(self.sideMenu_2)
        self.statsButton.setObjectName(u"statsButton")

        self.sideMenu.addWidget(self.statsButton)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sideMenu.addItem(self.verticalSpacer_3)

        self.sideMenuLine = QFrame(self.sideMenu_2)
        self.sideMenuLine.setObjectName(u"sideMenuLine")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.sideMenuLine.sizePolicy().hasHeightForWidth())
        self.sideMenuLine.setSizePolicy(sizePolicy3)
        self.sideMenuLine.setSizeIncrement(QSize(0, 0))
        self.sideMenuLine.setLineWidth(1)
        self.sideMenuLine.setMidLineWidth(0)
        self.sideMenuLine.setFrameShape(QFrame.Shape.HLine)
        self.sideMenuLine.setFrameShadow(QFrame.Shadow.Sunken)

        self.sideMenu.addWidget(self.sideMenuLine)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sideMenu.addItem(self.verticalSpacer)

        self.toolButtonContainer = QWidget(self.sideMenu_2)
        self.toolButtonContainer.setObjectName(u"toolButtonContainer")
        self.horizontalLayout_2 = QHBoxLayout(self.toolButtonContainer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.logModalButton = QToolButton(self.toolButtonContainer)
        self.logModalButton.setObjectName(u"logModalButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.WindowNew))
        self.logModalButton.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.logModalButton)

        self.appConfigButton = QToolButton(self.toolButtonContainer)
        self.appConfigButton.setObjectName(u"appConfigButton")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        self.appConfigButton.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.appConfigButton)

        self.manualButton = QToolButton(self.toolButtonContainer)
        self.manualButton.setObjectName(u"manualButton")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpFaq))
        self.manualButton.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.manualButton)


        self.sideMenu.addWidget(self.toolButtonContainer)

        self.sideMenu.setStretch(2, 1)

        self.gridLayout.addWidget(self.sideMenu_2, 0, 0, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 18))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.connectionMenuButton.setText(QCoreApplication.translate("MainWindow", u"Conex\u00e3o com joystick", None))
        self.calibrationButton.setText(QCoreApplication.translate("MainWindow", u"Calibra\u00e7\u00e3o", None))
        self.configButton.setText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00e3o de bot\u00f5es", None))
        self.gameProfileButton.setText(QCoreApplication.translate("MainWindow", u"Perfis de configura\u00e7\u00f5es", None))
        self.userActionsButton.setText(QCoreApplication.translate("MainWindow", u"A\u00e7\u00f5es de usu\u00e1rio", None))
        self.statsButton.setText(QCoreApplication.translate("MainWindow", u"Estat\u00edsticas de uso", None))
        self.logModalButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.appConfigButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.manualButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
    # retranslateUi

