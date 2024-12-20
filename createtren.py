from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Createtren(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(389, 292)
        Dialog.setMinimumSize(QtCore.QSize(389, 292))
        Dialog.setMaximumSize(QtCore.QSize(389, 292))
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: #e0f0ff\n"
"}")
        self.name_tren = QtWidgets.QLineEdit(Dialog)
        self.name_tren.setGeometry(QtCore.QRect(30, 40, 331, 31))
        self.name_tren.setStyleSheet("#name_tren {\n"
"background-color: #FFFFFF;\n"
"border-radius:5%;\n"
"}")
        self.name_tren.setFrame(True)
        self.name_tren.setDragEnabled(False)
        self.name_tren.setObjectName("name_tren")
        self.name_tren.setMaxLength(27)
        self.trenerBox_soztren = QtWidgets.QComboBox(Dialog)
        self.trenerBox_soztren.setGeometry(QtCore.QRect(27, 110, 336, 26))
        self.trenerBox_soztren.setEditable(True)
        self.trenerBox_soztren.setCurrentText("")
        self.trenerBox_soztren.setObjectName("trenerBox_soztren")
        self.grupaBox_soztren = QtWidgets.QComboBox(Dialog)
        self.grupaBox_soztren.setGeometry(QtCore.QRect(27, 170, 200, 26))
        self.grupaBox_soztren.setEditable(True)
        self.grupaBox_soztren.setObjectName("grupaBox_soztren")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(35, 90, 61, 16))
        self.label_2.setStyleSheet("#label_2 {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(35, 150, 61, 16))
        self.label_3.setStyleSheet("#label_3 {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label_3.setObjectName("label_3")
        self.dateTimeEdit_soztren = QtWidgets.QDateTimeEdit(Dialog)
        self.dateTimeEdit_soztren.setGeometry(QtCore.QRect(27, 210, 151, 24))
        self.dateTimeEdit_soztren.setWrapping(False)
        self.dateTimeEdit_soztren.setFrame(False)
        self.dateTimeEdit_soztren.setReadOnly(False)
        self.dateTimeEdit_soztren.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.dateTimeEdit_soztren.setSpecialValueText("")
        self.dateTimeEdit_soztren.setAccelerated(False)
        self.dateTimeEdit_soztren.setProperty("showGroupSeparator", False)
        self.dateTimeEdit_soztren.setMaximumDate(QtCore.QDate(2026, 12, 31))
        self.dateTimeEdit_soztren.setMinimumDate(QtCore.QDate(2024, 1, 1))
        self.dateTimeEdit_soztren.setCalendarPopup(True)
        self.dateTimeEdit_soztren.setObjectName("dateTimeEdit_soztren")
        self.addbutton_soztren = QtWidgets.QPushButton(Dialog)
        self.addbutton_soztren.setGeometry(QtCore.QRect(290, 250, 85, 25))
        self.addbutton_soztren.setStyleSheet("#addbutton_soztren {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#addbutton_soztren:hover {\n"
"background-color: #71bc78\n"
"}")
        self.addbutton_soztren.setObjectName("addbutton_soztren")
        self.cancelbutton_soztren = QtWidgets.QPushButton(Dialog)
        self.cancelbutton_soztren.setGeometry(QtCore.QRect(190, 250, 85, 25))
        self.cancelbutton_soztren.setStyleSheet("#cancelbutton_soztren {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#cancelbutton_soztren:hover {\n"
"background-color: #9db1cc\n"
"}")
        self.cancelbutton_soztren.setObjectName("cancelbutton_soztren")
        self.cancelbutton_soztren.clicked.connect(Dialog.close)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Создание тренировки"))
        self.name_tren.setPlaceholderText(_translate("Dialog", "Название тренировки..."))
        self.label_2.setText(_translate("Dialog", "Тренер:"))
        self.label_3.setText(_translate("Dialog", "Группа:"))
        self.addbutton_soztren.setText(_translate("Dialog", "Создать"))
        self.cancelbutton_soztren.setText(_translate("Dialog", "Отмена"))
