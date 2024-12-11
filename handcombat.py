import sys
import json
import os 
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import QDate
from mainwindow import Ui_Mainwindow
from createtren import Ui_Createtren

DATA_FILE = "data.json"

class LoginSystem(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('forms/loginform.ui', self)
        self.pushButton.clicked.connect(self.login)  
        self.pushButton_2.clicked.connect(self.logout)  

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

class MainWindow(QDialog):
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
        create_sportman = QDialog(self)
        uic.loadUi('forms/create_sportman.ui', create_sportman) 
        add_button = create_sportman.findChild(QtWidgets.QPushButton, "addbutton_sportman")
        cancel_button = create_sportman.findChild(QtWidgets.QPushButton, "cancelbutton_sportman")
        if add_button:
            add_button.clicked.connect(create_sportman.close) ##Добавление спортсмена в базу
        if cancel_button:
            cancel_button.clicked.connect(create_sportman.close)
        sportrazr_box = create_sportman.findChild(QtWidgets.QComboBox, "sportrazrBox")
        if sportrazr_box:
            add_items_lambda = lambda: sportrazr_box.addItems(["3ий юношевский", "2ой юнешевский", 
                                    "1ый юношевский", "3ий спортивный", 
                                    "2ий спортивный", "1ый спортивный", 
                                    "КМС", "МС", "МСМК", "ЗМС"])
            add_items_lambda()
        else:
            print("sportrazrBox не найден!")
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