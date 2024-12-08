import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox


class LoginSystem(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi('loginform.ui', self)

        self.pushButton.clicked.connect(self.login)  
        self.pushButton_2.clicked.connect(self.exit_system)  

    def login(self):
        username = self.lineEdit.text()  
        password = self.lineEdit_2.text()  

        if username == "admin" and password == "password":  
            QMessageBox.information(self, "Успех", "Вы успешно вошли в систему!")
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль!")

    def exit_system(self):
        self.close()

app = QApplication(sys.argv)
window = LoginSystem()
window.show()
sys.exit(app.exec_())
