from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditGruppa(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(595, 415)
        Dialog.setMinimumSize(QtCore.QSize(595, 415))
        Dialog.setMaximumSize(QtCore.QSize(595, 415))
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: #e0f0ff\n"
"}")
        self.cancelbutton_grupa = QtWidgets.QPushButton(parent=Dialog)
        self.cancelbutton_grupa.setGeometry(QtCore.QRect(370, 360, 85, 25))
        self.cancelbutton_grupa.setStyleSheet("#cancelbutton_grupa {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#cancelbutton_grupa:hover {\n"
"background-color: #9db1cc\n"
"}")
        self.cancelbutton_grupa.setObjectName("cancelbutton_grupa")
        self.comboBox_trener = QtWidgets.QComboBox(parent=Dialog)
        self.comboBox_trener.setGeometry(QtCore.QRect(28, 92, 337, 26))
        self.comboBox_trener.setObjectName("comboBox_trener")
        self.lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(400, 140, 151, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.addbutton_grupa = QtWidgets.QPushButton(parent=Dialog)
        self.addbutton_grupa.setGeometry(QtCore.QRect(480, 360, 85, 25))
        self.addbutton_grupa.setStyleSheet("#addbutton_grupa {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#addbutton_grupa:hover {\n"
"background-color: #71bc78\n"
"}")
        self.addbutton_grupa.setObjectName("addbutton_grupa")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(30, 70, 60, 16))
        self.label.setStyleSheet("#label {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label.setObjectName("label")
        self.listWidget_spotsmans = QtWidgets.QListWidget(parent=Dialog)
        self.listWidget_spotsmans.setGeometry(QtCore.QRect(30, 130, 535, 211))
        self.listWidget_spotsmans.setStyleSheet("")
        self.listWidget_spotsmans.setObjectName("listWidget_spotsmans")
        self.name_grupa = QtWidgets.QLineEdit(parent=Dialog)
        self.name_grupa.setGeometry(QtCore.QRect(30, 20, 331, 25))
        self.name_grupa.setStyleSheet("#name_grupa {\n"
"background-color: #FFFFFF;\n"
"border-radius:5%;\n"
"}")
        self.name_grupa.setMaxLength(35)
        self.name_grupa.setObjectName("name_grupa")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменение группы"))
        self.cancelbutton_grupa.setText(_translate("Dialog", "Отмена"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Поиск..."))
        self.addbutton_grupa.setText(_translate("Dialog", "Сохранить"))
        self.label.setText(_translate("Dialog", "Тренер:"))
        self.name_grupa.setPlaceholderText(_translate("Dialog", "Название группы"))
