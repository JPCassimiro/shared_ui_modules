# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calibration_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QWidget)

from shared_ui_modules.ui.model.custom_widgets.rounded_image_label import RoundedImageLabel

class Ui_calibrationForm(object):
    def setupUi(self, calibrationForm):
        if not calibrationForm.objectName():
            calibrationForm.setObjectName(u"calibrationForm")
        calibrationForm.resize(522, 485)
        self.gridLayout = QGridLayout(calibrationForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.calibrationWidgetContainer = QWidget(calibrationForm)
        self.calibrationWidgetContainer.setObjectName(u"calibrationWidgetContainer")
        self.gridLayout_2 = QGridLayout(self.calibrationWidgetContainer)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.buttonsContainer = QWidget(self.calibrationWidgetContainer)
        self.buttonsContainer.setObjectName(u"buttonsContainer")
        self.gridLayout_5 = QGridLayout(self.buttonsContainer)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.restartButton = QPushButton(self.buttonsContainer)
        self.restartButton.setObjectName(u"restartButton")

        self.gridLayout_5.addWidget(self.restartButton, 2, 0, 1, 1)

        self.cancelButton = QPushButton(self.buttonsContainer)
        self.cancelButton.setObjectName(u"cancelButton")

        self.gridLayout_5.addWidget(self.cancelButton, 1, 0, 1, 1)

        self.startButton = QPushButton(self.buttonsContainer)
        self.startButton.setObjectName(u"startButton")

        self.gridLayout_5.addWidget(self.startButton, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 1, 1, 1, 1)


        self.gridLayout_2.addWidget(self.buttonsContainer, 2, 0, 1, 1)

        self.visualsContainer = QWidget(self.calibrationWidgetContainer)
        self.visualsContainer.setObjectName(u"visualsContainer")
        self.gridLayout_4 = QGridLayout(self.visualsContainer)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.stackedWidget = QStackedWidget(self.visualsContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.instructionsPage = QWidget()
        self.instructionsPage.setObjectName(u"instructionsPage")
        self.gridLayout_3 = QGridLayout(self.instructionsPage)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.imgLabel = RoundedImageLabel(self.instructionsPage)
        self.imgLabel.setObjectName(u"imgLabel")
        self.imgLabel.setMaximumSize(QSize(300, 350))

        self.gridLayout_3.addWidget(self.imgLabel, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 1, 1, 1)

        self.instructionLabel = QLabel(self.instructionsPage)
        self.instructionLabel.setObjectName(u"instructionLabel")
        self.instructionLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.instructionLabel.setWordWrap(True)

        self.gridLayout_3.addWidget(self.instructionLabel, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(158, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 3, 1, 1)

        self.stackedWidget.addWidget(self.instructionsPage)
        self.resultsPage = QWidget()
        self.resultsPage.setObjectName(u"resultsPage")
        self.stackedWidget.addWidget(self.resultsPage)

        self.gridLayout_4.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.visualsContainer, 0, 0, 1, 1)

        self.gridLayout_2.setRowStretch(0, 1)

        self.gridLayout.addWidget(self.calibrationWidgetContainer, 0, 0, 1, 1)


        self.retranslateUi(calibrationForm)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(calibrationForm)
    # setupUi

    def retranslateUi(self, calibrationForm):
        calibrationForm.setWindowTitle(QCoreApplication.translate("calibrationForm", u"Form", None))
        self.restartButton.setText(QCoreApplication.translate("calibrationForm", u"Reiniciar", None))
        self.cancelButton.setText(QCoreApplication.translate("calibrationForm", u"Cancelar", None))
        self.startButton.setText(QCoreApplication.translate("calibrationForm", u"Iniciar", None))
        self.imgLabel.setText(QCoreApplication.translate("calibrationForm", u"imageLabel", None))
        self.instructionLabel.setText(QCoreApplication.translate("calibrationForm", u"instructionLabel", None))
    # retranslateUi

