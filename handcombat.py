import sys
import json
import os 
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

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

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi('forms/mainwindow.ui', self)

        exit_button = self.findChild(QtWidgets.QPushButton, "pushButton")
        if exit_button:
            exit_button.clicked.connect(self.confirm_exit)

        self.login_window = LoginSystem()
        if self.login_window.exec_() != QDialog.Accepted:
            return  
        self.show()
    
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