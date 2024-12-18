from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditSportman(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(620, 292)
        Dialog.setMinimumSize(QtCore.QSize(620, 292))
        Dialog.setMaximumSize(QtCore.QSize(620, 292))
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: #e0f0ff\n"
"}\n"
"")
        self.addbutton_sportman = QtWidgets.QPushButton(parent=Dialog)
        self.addbutton_sportman.setGeometry(QtCore.QRect(511, 245, 85, 25))
        self.addbutton_sportman.setStyleSheet("#addbutton_sportman {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#addbutton_sportman:hover {\n"
"background-color: #71bc78\n"
"}")
        self.addbutton_sportman.setObjectName("addbutton_sportman")
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 175, 161, 16))
        self.label_3.setStyleSheet("#label_3 {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label_3.setObjectName("label_3")
        self.datebirth_sportman = QtWidgets.QDateEdit(parent=Dialog)
        self.datebirth_sportman.setGeometry(QtCore.QRect(18, 141, 110, 24))
        self.datebirth_sportman.setObjectName("datebirth_sportman")
        self.grupaBox_sportman = QtWidgets.QComboBox(parent=Dialog)
        self.grupaBox_sportman.setGeometry(QtCore.QRect(16, 85, 260, 26))
        self.grupaBox_sportman.setEditable(False)
        self.grupaBox_sportman.setObjectName("grupaBox_sportman")
        self.cancelbutton_sportman = QtWidgets.QPushButton(parent=Dialog)
        self.cancelbutton_sportman.setGeometry(QtCore.QRect(406, 245, 85, 25))
        self.cancelbutton_sportman.setStyleSheet("#cancelbutton_sportman {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#cancelbutton_sportman:hover {\n"
"background-color: #9db1cc\n"
"}")
        self.cancelbutton_sportman.setObjectName("cancelbutton_sportman")
        self.name_sportman = QtWidgets.QLineEdit(parent=Dialog)
        self.name_sportman.setGeometry(QtCore.QRect(16, 25, 180, 25))
        self.name_sportman.setStyleSheet("#name_sportman {\n"
"background-color: #FFFFFF;\n"
"border-radius:5%;\n"
"}")
        self.name_sportman.setObjectName("name_sportman")
        self.sportrazrBox = QtWidgets.QComboBox(parent=Dialog)
        self.sportrazrBox.setGeometry(QtCore.QRect(16, 198, 260, 26))
        self.sportrazrBox.setEditable(False)
        self.sportrazrBox.setObjectName("sportrazrBox")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(20, 65, 60, 16))
        self.label.setStyleSheet("#label {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label.setObjectName("label")
        self.surname_sportman = QtWidgets.QLineEdit(parent=Dialog)
        self.surname_sportman.setGeometry(QtCore.QRect(216, 25, 180, 25))
        self.surname_sportman.setStyleSheet("#surname_sportman{\n"
"background-color: #FFFFFF;\n"
"border-radius:5%;\n"
"}")
        self.surname_sportman.setObjectName("surname_sportman")
        self.otchestvo_sportman = QtWidgets.QLineEdit(parent=Dialog)
        self.otchestvo_sportman.setGeometry(QtCore.QRect(416, 25, 180, 25))
        self.otchestvo_sportman.setStyleSheet("#otchestvo_sportman {\n"
"background-color: #FFFFFF;\n"
"border-radius:5%;\n"
"}")
        self.otchestvo_sportman.setObjectName("otchestvo_sportman")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 161, 16))
        self.label_2.setStyleSheet("#label_2 {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменение данных спортсмена"))
        self.addbutton_sportman.setText(_translate("Dialog", "Добавить"))
        self.label_3.setText(_translate("Dialog", "Спортивный разряд:"))
        self.cancelbutton_sportman.setText(_translate("Dialog", "Отмена"))
        self.name_sportman.setPlaceholderText(_translate("Dialog", "Фамилия"))
        self.label.setText(_translate("Dialog", "Группа:"))
        self.surname_sportman.setPlaceholderText(_translate("Dialog", "Имя"))
        self.otchestvo_sportman.setPlaceholderText(_translate("Dialog", "Отчество"))
        self.label_2.setText(_translate("Dialog", "Дата рождения:"))
