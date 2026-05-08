# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_actions_widget.ui'
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
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QToolButton, QVBoxLayout,
    QWidget)

class Ui_usersWidgetForm(object):
    def setupUi(self, usersWidgetForm):
        if not usersWidgetForm.objectName():
            usersWidgetForm.setObjectName(u"usersWidgetForm")
        usersWidgetForm.resize(745, 520)
        self.gridLayout = QGridLayout(usersWidgetForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabContainer = QWidget(usersWidgetForm)
        self.tabContainer.setObjectName(u"tabContainer")
        self.horizontalLayout = QHBoxLayout(self.tabContainer)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.tabContainer)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.TabShape.Triangular)
        self.therapistTab = QWidget()
        self.therapistTab.setObjectName(u"therapistTab")
        self.gridLayout_2 = QGridLayout(self.therapistTab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.therapistListContainer = QWidget(self.therapistTab)
        self.therapistListContainer.setObjectName(u"therapistListContainer")
        self.gridLayout_3 = QGridLayout(self.therapistListContainer)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.buttonContainer1 = QWidget(self.therapistListContainer)
        self.buttonContainer1.setObjectName(u"buttonContainer1")
        self.horizontalLayout_3 = QHBoxLayout(self.buttonContainer1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit1 = QLineEdit(self.buttonContainer1)
        self.lineEdit1.setObjectName(u"lineEdit1")

        self.horizontalLayout_3.addWidget(self.lineEdit1)

        self.toolButton1 = QToolButton(self.buttonContainer1)
        self.toolButton1.setObjectName(u"toolButton1")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.toolButton1.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.toolButton1)

        self.defautlTherapistButton = QPushButton(self.buttonContainer1)
        self.defautlTherapistButton.setObjectName(u"defautlTherapistButton")

        self.horizontalLayout_3.addWidget(self.defautlTherapistButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.gridLayout_3.addWidget(self.buttonContainer1, 0, 0, 1, 1)

        self.listWidget1 = QListWidget(self.therapistListContainer)
        self.listWidget1.setObjectName(u"listWidget1")

        self.gridLayout_3.addWidget(self.listWidget1, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.therapistListContainer, 0, 0, 1, 1)

        self.tabWidget.addTab(self.therapistTab, "")
        self.patientTab = QWidget()
        self.patientTab.setObjectName(u"patientTab")
        self.gridLayout_4 = QGridLayout(self.patientTab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.patientListContainer = QWidget(self.patientTab)
        self.patientListContainer.setObjectName(u"patientListContainer")
        self.verticalLayout = QVBoxLayout(self.patientListContainer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.buttonContainer2 = QWidget(self.patientListContainer)
        self.buttonContainer2.setObjectName(u"buttonContainer2")
        self.horizontalLayout_2 = QHBoxLayout(self.buttonContainer2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit2 = QLineEdit(self.buttonContainer2)
        self.lineEdit2.setObjectName(u"lineEdit2")

        self.horizontalLayout_2.addWidget(self.lineEdit2)

        self.toolButton2 = QToolButton(self.buttonContainer2)
        self.toolButton2.setObjectName(u"toolButton2")
        self.toolButton2.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.toolButton2)

        self.defaultPatientButton = QPushButton(self.buttonContainer2)
        self.defaultPatientButton.setObjectName(u"defaultPatientButton")

        self.horizontalLayout_2.addWidget(self.defaultPatientButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.buttonContainer2)

        self.listWidget2 = QListWidget(self.patientListContainer)
        self.listWidget2.setObjectName(u"listWidget2")

        self.verticalLayout.addWidget(self.listWidget2)


        self.gridLayout_4.addWidget(self.patientListContainer, 0, 0, 1, 1)

        self.tabWidget.addTab(self.patientTab, "")

        self.horizontalLayout.addWidget(self.tabWidget)


        self.gridLayout.addWidget(self.tabContainer, 0, 1, 1, 1)


        self.retranslateUi(usersWidgetForm)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(usersWidgetForm)
    # setupUi

    def retranslateUi(self, usersWidgetForm):
        usersWidgetForm.setWindowTitle(QCoreApplication.translate("usersWidgetForm", u"Form", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("usersWidgetForm", u"Cadastrar um novo paciente", u"UserActionsHelper"))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.toolButton1.setToolTip(QCoreApplication.translate("usersWidgetForm", u"Cadastrar um novo terapeuta", u"UserActionsHelper"))
#endif // QT_CONFIG(tooltip)
        self.toolButton1.setText(QCoreApplication.translate("usersWidgetForm", u"...", None))
#if QT_CONFIG(tooltip)
        self.defautlTherapistButton.setToolTip(QCoreApplication.translate("usersWidgetForm", u"Retornar ao valor de terapeuta padr\u00e3o", u"UserActionsHelper"))
#endif // QT_CONFIG(tooltip)
        self.defautlTherapistButton.setText(QCoreApplication.translate("usersWidgetForm", u"Terapeuta padr\u00e3o", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.therapistTab), QCoreApplication.translate("usersWidgetForm", u"Terapeuta", None))
        self.toolButton2.setText(QCoreApplication.translate("usersWidgetForm", u"...", None))
#if QT_CONFIG(tooltip)
        self.defaultPatientButton.setToolTip(QCoreApplication.translate("usersWidgetForm", u"Retornar ao valor de paciente padr\u00e3o", u"UserActionsHelper"))
#endif // QT_CONFIG(tooltip)
        self.defaultPatientButton.setText(QCoreApplication.translate("usersWidgetForm", u"Paciente padr\u00e3o", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.patientTab), QCoreApplication.translate("usersWidgetForm", u"Paciente", None))
    # retranslateUi

