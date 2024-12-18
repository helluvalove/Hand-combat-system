from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditCoach(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(620, 250)
        Dialog.setMinimumSize(QtCore.QSize(620, 250))
        Dialog.setMaximumSize(QtCore.QSize(620, 250))
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: #e0f0ff\n"
"}\n"
"")
        self.dopinfo_coach = QtWidgets.QPlainTextEdit(parent=Dialog)
        self.dopinfo_coach.setGeometry(QtCore.QRect(20, 70, 581, 121))
        self.dopinfo_coach.setStyleSheet("#dopinfo_coach {\n"
"background-color: #FFFFFF;\n"
"border-radius:5%;\n"
"}")
        self.dopinfo_coach.setMaximumBlockCount(1)
        self.dopinfo_coach.setBackgroundVisible(False)
        self.dopinfo_coach.setCenterOnScroll(False)
        self.dopinfo_coach.setObjectName("dopinfo_coach")
        self.otchestvo_coach = QtWidgets.QLineEdit(parent=Dialog)
        self.otchestvo_coach.setGeometry(QtCore.QRect(420, 30, 180, 25))
        self.otchestvo_coach.setStyleSheet("#otchestvo_coach {\n"
"background-color: #FFFFFF;\n"
"border-radius:5%;\n"
"}")
        self.otchestvo_coach.setObjectName("otchestvo_coach")
        self.otchestvo_coach.setMaxLength(25)
        self.cancelbutton_coach = QtWidgets.QPushButton(parent=Dialog)
        self.cancelbutton_coach.setGeometry(QtCore.QRect(410, 210, 85, 25))
        self.cancelbutton_coach.setStyleSheet("#cancelbutton_coach {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#cancelbutton_coach:hover {\n"
"background-color: #9db1cc\n"
"}")
        self.cancelbutton_coach.setObjectName("cancelbutton_coach")
        self.name_coach = QtWidgets.QLineEdit(parent=Dialog)
        self.name_coach.setGeometry(QtCore.QRect(20, 30, 180, 25))
        self.name_coach.setStyleSheet("#name_coach {\n"
"background-color: #FFFFFF;\n"
"border-radius:5%;\n"
"}")
        self.name_coach.setObjectName("name_coach")
        self.name_coach.setMaxLength(25)
        self.surname_coach = QtWidgets.QLineEdit(parent=Dialog)
        self.surname_coach.setGeometry(QtCore.QRect(220, 30, 180, 25))
        self.surname_coach.setStyleSheet("#surname_coach {\n"
"background-color: #FFFFFF;\n"
"border-radius:5%;\n"
"}")
        self.surname_coach.setObjectName("surname_coach")
        self.surname_coach.setMaxLength(25)
        self.addbutton_coach = QtWidgets.QPushButton(parent=Dialog)
        self.addbutton_coach.setGeometry(QtCore.QRect(515, 210, 85, 25))
        self.addbutton_coach.setStyleSheet("#addbutton_coach {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#addbutton_coach:hover {\n"
"background-color: #71bc78\n"
"}")
        self.addbutton_coach.setObjectName("addbutton_coach")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменение данных тренера"))
        self.dopinfo_coach.setPlaceholderText(_translate("Dialog", "Дополнительная информация о тренере"))
        self.otchestvo_coach.setPlaceholderText(_translate("Dialog", "Отчество"))
        self.cancelbutton_coach.setText(_translate("Dialog", "Отмена"))
        self.name_coach.setPlaceholderText(_translate("Dialog", "Фамилия"))
        self.surname_coach.setPlaceholderText(_translate("Dialog", "Имя"))
        self.addbutton_coach.setText(_translate("Dialog", "Сохранить"))
