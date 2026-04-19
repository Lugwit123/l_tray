# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setEnvVar.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(518, 84)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(180, 16777215))

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(180, 16777215))
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label.setWordWrap(False)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u8bbe\u7f6e\u73af\u5883\u53d8\u91cf", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Lugwit_publicPath:", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Form", u"A:\\TD", None))
        self.label.setText(QCoreApplication.translate("Form", u"TD_Depot", None))
        self.lineEdit.setText(QCoreApplication.translate("Form", u"D:\\TD_Depot", None))
    # retranslateUi

