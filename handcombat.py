import sys
import json
import os 
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow
# from PyQt5.QtGui import QTextCharFormat, QColor
# from PyQt5.QtCore import QDate
from mainwindow import Ui_Mainwindow
from createtren import Ui_Createtren
from create_sportman import Ui_SportMan
from create_gruppa import Ui_CreateGruppa

DATA_FILE = "data.json"

class LoginSystem(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('forms/loginform.ui', self)
        self.pushButton.clicked.connect(self.login)  
        self.pushButton_2.clicked.connect(self.logout)  

        no_space_validator = QRegExpValidator(QRegExp(r"[^\s]*"))
        self.lineEdit.setValidator(no_space_validator)
        self.lineEdit_2.setValidator(no_space_validator)

        self.lineEdit.setMaxLength(15)  
        self.lineEdit_2.setMaxLength(20)

    def login(self):
        username = self.lineEdit.text()  
        password = self.lineEdit_2.text()  
        if username == "admin" and password == "password":
            self.accept()
        else:
            self.show_error_dialog()

    def logout(self):
        logout_dialog = QDialog(self)
        uic.loadUi('forms/logoutsystem.ui', logout_dialog)
        da_button = logout_dialog.findChild(QtWidgets.QPushButton, "pushButton_2")
        net_button = logout_dialog.findChild(QtWidgets.QPushButton, "pushButton")
        if da_button:
            da_button.clicked.connect(self.exit_system)
        if net_button:
            net_button.clicked.connect(logout_dialog.close)
        logout_dialog.exec_()     

    def show_error_dialog(self):
        error_dialog = QDialog(self)
        uic.loadUi('forms/errorlogin.ui', error_dialog)
        ok_button = error_dialog.findChild(QtWidgets.QPushButton, "pushButton")
        if ok_button:
            ok_button.clicked.connect(error_dialog.close)
        error_dialog.exec_()

    def exit_system(self):
        self.close()

class CreateTren(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Createtren()
        self.ui.setupUi(self)

class SportManDialog(QDialog, Ui_SportMan):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setup_widgets()

        self.addbutton_sportman.clicked.connect(self.on_add_clicked)
        self.cancelbutton_sportman.clicked.connect(self.reject)

    def setup_widgets(self):
        self.sportrazrBox.addItem("")
        self.sportrazrBox.addItems([
            "3ий юношеский", "2ой юношеский", "1ый юношеский",
            "3ий спортивный", "2ой спортивный", "1ый спортивный",
            "КМС", "МС", "МСМК", "ЗМС"
        ])

        self.datebirth_sportman.setCalendarPopup(True)

    def on_add_clicked(self):
        name = self.name_sportman.text()
        surname = self.surname_sportman.text()
        otchestvo = self.otchestvo_sportman.text()
        grupa = self.grupaBox_sportman.currentText()
        datebirth = self.datebirth_sportman.date().toString("yyyy-MM-dd")
        sportrazr = self.sportrazrBox.currentText()

        if not name or not surname or not grupa:
            QMessageBox.warning(self, "Ошибка", "Все обязательные поля должны быть заполнены!")
            return

        if sportrazr == "":
            QMessageBox.warning(self, "Ошибка", "Выберите спортивный разряд!")
            return

        print(f"Добавлен спортсмен: {surname} {name} {otchestvo}, группа: {grupa}, "
              f"дата рождения: {datebirth}, разряд: {sportrazr}")

        self.accept()

class CreateGruppaDialog(QDialog, Ui_CreateGruppa):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  
        self.setup_widgets()

        self.addbutton_grupa.clicked.connect(self.on_add_clicked)
        self.cancelbutton_grupa.clicked.connect(self.reject)

    def setup_widgets(self):
        self.comboBox_trener.addItem("Выберите тренера")
        self.comboBox_trener.addItems(["Тренер 1", "Тренер 2", "Тренер 3"])
        self.comboBox_trener.setCurrentIndex(0)

    def on_add_clicked(self):
        name = self.name_grupa.text()
        trener = self.comboBox_trener.currentText()

        if not name or trener == "Выберите тренера":
            QMessageBox.warning(self, "Ошибка", "Все обязательные поля должны быть заполнены!")
            return

        print(f"Добавлена группа: {name}, тренер: {trener}")
        self.accept()

class MainWindow(QDialog, Ui_Mainwindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Mainwindow()
        self.ui.setupUi(self)  
        exit_button = self.ui.exitButton
        if exit_button:
            exit_button.clicked.connect(self.confirm_exit)

        self.ui.addbutton_tab2.clicked.connect(self.open_create_tren_dialog)
        self.ui.izmenbutton_tab2.clicked.connect(self.open_create_tren_dialog)
        self.ui.delbutton_tab2.clicked.connect(self.del_tren_dialog)

        self.ui.addbutton_tab3.clicked.connect(self.create_coach_dialog)
        self.ui.izmenbutton_tab3.clicked.connect(self.create_coach_dialog)
        self.ui.delbutton_tab3.clicked.connect(self.del_coach_dialog)

        self.ui.addbutton_tab4.clicked.connect(self.create_sportman_dialog)
        self.ui.izmenbutton_tab4.clicked.connect(self.create_sportman_dialog)
        self.ui.delbutton_tab4.clicked.connect(self.del_sportman_dialog)

        self.ui.addbutton_tab5.clicked.connect(self.create_gruppa_dialog)
        self.ui.izmenbutton_tab5.clicked.connect(self.create_gruppa_dialog)
        self.ui.delbutton_tab5.clicked.connect(self.del_gruppa_dialog)

        self.ui.clearbutton_tab6.clicked.connect(self.del_otchet_dialog)

        self.login_window = LoginSystem()
        if self.login_window.exec_() != QDialog.Accepted:
            return  
        self.show()

    def open_create_tren_dialog(self):
        create_tren_dialog = CreateTren(self)
        create_tren_dialog.exec_()

    def del_tren_dialog(self):
        del_tren = QDialog(self)
        uic.loadUi('forms/deleteconfirm.ui', del_tren)
        yes_button = del_tren.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_tren.findChild(QtWidgets.QPushButton, "pushButton")
        if yes_button:
            yes_button.clicked.connect(del_tren.close) ##Удаление записи о тренировке
        if no_button:
            no_button.clicked.connect(del_tren.close)
        del_tren.exec_()

    def create_coach_dialog(self):
        create_coach = QDialog(self)
        uic.loadUi('forms/create_coach.ui', create_coach)
        add_button = create_coach.findChild(QtWidgets.QPushButton, "addbutton_coach")
        cancel_button = create_coach.findChild(QtWidgets.QPushButton, "cancelbutton_coach")
        if add_button:
            add_button.clicked.connect(create_coach.close) ##Добавление тренера в базу
        if cancel_button:
            cancel_button.clicked.connect(create_coach.close)
        create_coach.exec_()

    def del_coach_dialog(self):
        del_coach = QDialog(self)
        uic.loadUi('forms/delcoach.ui', del_coach)
        yes_button = del_coach.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_coach.findChild(QtWidgets.QPushButton, "pushButton")
        if yes_button:
            yes_button.clicked.connect(del_coach.close) ##Удаляет тренера из базы
        if no_button:
            no_button.clicked.connect(del_coach.close)
        del_coach.exec_()

    def create_sportman_dialog(self):
        create_sportman = SportManDialog(self)  
        create_sportman.exec_()

    def del_sportman_dialog(self):
        del_sportman = QDialog(self)
        uic.loadUi('forms/delsportman.ui', del_sportman)
        yes_button = del_sportman.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_sportman.findChild(QtWidgets.QPushButton, "pushButton")
        if yes_button:
            yes_button.clicked.connect(del_sportman.close) ##Удаляет спортсмена из базы
        if no_button:
            no_button.clicked.connect(del_sportman.close)
        del_sportman.exec_()

    def create_gruppa_dialog(self):
        create_gruppa = CreateGruppaDialog(self)
        create_gruppa.exec_()

    def del_gruppa_dialog(self):
        del_gruppa = QDialog(self)
        uic.loadUi('forms/del_gruppa.ui', del_gruppa)
        yes_button = del_gruppa.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_gruppa.findChild(QtWidgets.QPushButton, "pushButton")
        if yes_button:
            yes_button.clicked.connect(del_gruppa.close) ## Удаляет группу из базы
        if no_button:
            no_button.clicked.connect(del_gruppa.close)
        del_gruppa.exec_()

    def del_otchet_dialog(self):
        del_otchet = QDialog(self)
        uic.loadUi('forms/del_otchet.ui', del_otchet)
        yes_button = del_otchet.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_otchet.findChild(QtWidgets.QPushButton, "pushButton")
        if yes_button:
            yes_button.clicked.connect(del_otchet.close) ##Очищает поля отчетов
        if no_button:
            no_button.clicked.connect(del_otchet.close)
        del_otchet.exec_()

    def confirm_exit(self):
        logout_dialog = QDialog(self)
        uic.loadUi('forms/logoutsystem.ui', logout_dialog)
        yes_button = logout_dialog.findChild(QtWidgets.QPushButton, "pushButton_2")  
        no_button = logout_dialog.findChild(QtWidgets.QPushButton, "pushButton")    
        if yes_button:
            yes_button.clicked.connect(self.close)
        if no_button:
            no_button.clicked.connect(logout_dialog.close)
        logout_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())