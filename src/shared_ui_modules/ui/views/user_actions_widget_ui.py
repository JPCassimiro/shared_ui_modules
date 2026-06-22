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
        self.therapistButtonContainer = QWidget(self.therapistListContainer)
        self.therapistButtonContainer.setObjectName(u"therapistButtonContainer")
        self.horizontalLayout_3 = QHBoxLayout(self.therapistButtonContainer)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.therapistLineEdit = QLineEdit(self.therapistButtonContainer)
        self.therapistLineEdit.setObjectName(u"therapistLineEdit")

        self.horizontalLayout_3.addWidget(self.therapistLineEdit)

        self.addTherapistButton = QToolButton(self.therapistButtonContainer)
        self.addTherapistButton.setObjectName(u"addTherapistButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.addTherapistButton.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.addTherapistButton)

        self.defautlTherapistButton = QPushButton(self.therapistButtonContainer)
        self.defautlTherapistButton.setObjectName(u"defautlTherapistButton")

        self.horizontalLayout_3.addWidget(self.defautlTherapistButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.gridLayout_3.addWidget(self.therapistButtonContainer, 0, 0, 1, 1)

        self.therapistListWidget = QListWidget(self.therapistListContainer)
        self.therapistListWidget.setObjectName(u"therapistListWidget")

        self.gridLayout_3.addWidget(self.therapistListWidget, 1, 0, 1, 1)


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
        self.patientButtonContainer = QWidget(self.patientListContainer)
        self.patientButtonContainer.setObjectName(u"patientButtonContainer")
        self.horizontalLayout_2 = QHBoxLayout(self.patientButtonContainer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.patientLineEdit = QLineEdit(self.patientButtonContainer)
        self.patientLineEdit.setObjectName(u"patientLineEdit")

        self.horizontalLayout_2.addWidget(self.patientLineEdit)

        self.addPatientButton = QToolButton(self.patientButtonContainer)
        self.addPatientButton.setObjectName(u"addPatientButton")
        self.addPatientButton.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.addPatientButton)

        self.defaultPatientButton = QPushButton(self.patientButtonContainer)
        self.defaultPatientButton.setObjectName(u"defaultPatientButton")

        self.horizontalLayout_2.addWidget(self.defaultPatientButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.patientButtonContainer)

        self.patientListWidget = QListWidget(self.patientListContainer)
        self.patientListWidget.setObjectName(u"patientListWidget")

        self.verticalLayout.addWidget(self.patientListWidget)


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
        self.addTherapistButton.setToolTip(QCoreApplication.translate("usersWidgetForm", u"Cadastrar um novo terapeuta", u"UserActionsHelper"))
#endif // QT_CONFIG(tooltip)
        self.addTherapistButton.setText(QCoreApplication.translate("usersWidgetForm", u"...", None))
#if QT_CONFIG(tooltip)
        self.defautlTherapistButton.setToolTip(QCoreApplication.translate("usersWidgetForm", u"Retornar ao valor de terapeuta padr\u00e3o", u"UserActionsHelper"))
#endif // QT_CONFIG(tooltip)
        self.defautlTherapistButton.setText(QCoreApplication.translate("usersWidgetForm", u"Terapeuta padr\u00e3o", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.therapistTab), QCoreApplication.translate("usersWidgetForm", u"Terapeuta", None))
        self.addPatientButton.setText(QCoreApplication.translate("usersWidgetForm", u"...", None))
#if QT_CONFIG(tooltip)
        self.defaultPatientButton.setToolTip(QCoreApplication.translate("usersWidgetForm", u"Retornar ao valor de paciente padr\u00e3o", u"UserActionsHelper"))
#endif // QT_CONFIG(tooltip)
        self.defaultPatientButton.setText(QCoreApplication.translate("usersWidgetForm", u"Paciente padr\u00e3o", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.patientTab), QCoreApplication.translate("usersWidgetForm", u"Paciente", None))
    # retranslateUi

