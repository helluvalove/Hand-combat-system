import sys
import pymysql
import os 
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QPushButton, QTableWidgetItem, QHeaderView, QTableWidget
from database import DatabaseManager
from mainwindow import Ui_Mainwindow
from createtren import Ui_Createtren
from create_sportman import Ui_SportMan
from create_gruppa import Ui_CreateGruppa
from create_coach import Ui_CreateCoach
from edit_coach import Ui_EditCoach

def connect_to_db():
    try:
        connection = pymysql.connect(
            host="localhost",      
            user="root",  
            password="qwerty123",  
            database="hand_combat",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Успешное подключение к базе данных!")
        return connection
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

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
        connection = connect_to_db()  # Подключаемся к БД
        if not connection:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных!")
            return

        try:
            with connection.cursor() as cursor:
                # Запрос для поиска пользователя по логину
                query = "SELECT password FROM admin_user WHERE login = %s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()  # Получаем первую строку результата

                if result:
                    # Сравнение пароля (с хэшированием)
                    stored_password = result['password']
                    if password == stored_password:  # Для хэшированных паролей нужно использовать bcrypt
                        self.accept()
                    else:
                        self.show_error_dialog()
                else:
                    self.show_error_dialog()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка запроса к базе данных: {e}")
        finally:
            connection.close()

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
        logout_dialog = self.logout_dialog()
        logout_dialog.exec_()
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

class CreateCoachDialog(QDialog, Ui_CreateCoach):
    def __init__(self, db_manager, parent=None, view_mode=False):
        super().__init__(parent)
        self.setupUi(self)  # Задаём интерфейс через метод setupUi
        self.db_manager = db_manager
        self.view_mode = view_mode

        # Подключаем обработчики событий
        self.addbutton_coach.clicked.connect(self.add_coach_to_db)
        self.cancelbutton_coach.clicked.connect(self.reject)

        if self.view_mode:
            # Блокируем поля для редактирования и кнопку "Добавить"
            self.surname_coach.setReadOnly(True)
            self.name_coach.setReadOnly(True)
            self.otchestvo_coach.setReadOnly(True)
            self.dopinfo_coach.setReadOnly(True)
            self.add_button = self.findChild(QPushButton, "addbutton_coach")
            if self.add_button:
                self.add_button.setEnabled(False)  # Блокируем кнопку "Добавить"

    def add_coach_to_db(self):
        # Получаем данные из полей ввода
        surname = self.surname_coach.text().strip()
        name = self.name_coach.text().strip()
        patronymic = self.otchestvo_coach.text().strip()
        info = self.dopinfo_coach.toPlainText().strip()

        # Проверяем обязательные поля
        if not surname or not name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и Имя обязательны для заполнения!")
            return False  # Возвращаем False если проверка не пройдена

        # Продолжаем только если не в режиме просмотра
        if not self.view_mode:
            try:
                query = """
                INSERT INTO Тренера (Фамилия, Имя, Отчество, Доп_информация)
                VALUES (%s, %s, %s, %s)
                """
                params = (surname, name, patronymic, info)
                self.db_manager.execute_query(query, params)

                # Очищаем поля ввода
                self.surname_coach.clear()
                self.name_coach.clear()
                self.otchestvo_coach.clear()
                self.dopinfo_coach.clear()

                # Обновляем таблицу и закрываем окно
                if self.parent():
                    self.parent().load_trainers()
                self.accept()
                return True  # Возвращаем True при успешном добавлении

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить тренера: {e}")
                return False  # Возвращаем False при ошибке

    def closeEvent(self, event):
        if self.parent() and hasattr(self.parent(), "load_trainers"):
            self.parent().load_trainers()
        super().closeEvent(event)
    
class EditCoachDialog(QDialog, Ui_EditCoach):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Задаём интерфейс через метод setupUi
        self.db_manager = db_manager
        self.current_coach_id = None

        self.addbutton_coach.clicked.connect(self.save_coach_changes)
        self.cancelbutton_coach.clicked.connect(self.reject)

    def set_coach_data(self, coach_id, surname, name, patronymic, info):
        self.current_coach_id = coach_id
        self.surname_coach.setText(surname)
        self.name_coach.setText(name)
        self.otchestvo_coach.setText(patronymic)
        self.dopinfo_coach.setPlainText(info)

    def save_coach_changes(self):
        # Получаем новые данные из полей
        new_surname = self.surname_coach.text().strip()
        new_name = self.name_coach.text().strip()
        new_patronymic = self.otchestvo_coach.text().strip()
        new_info = self.dopinfo_coach.toPlainText().strip()

        # Проверяем обязательные поля
        if not new_surname or not new_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и Имя обязательны для заполнения!")
            return

        # Обновляем данные тренера
        update_query = """
        UPDATE Тренера SET Фамилия = %s, Имя = %s, Отчество = %s, Доп_информация = %s WHERE id_Тренера = %s
        """
        if self.db_manager.execute_query(update_query, (new_surname, new_name, new_patronymic, new_info, self.current_coach_id)):
            self.accept()  # Закрыть диалоговое окно
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные. Возможно, они не изменились.")

class MainWindow(QDialog, Ui_Mainwindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db_manager = DatabaseManager(
            host="127.0.0.1",
            user="root",
            password="qwerty123",
            db_name="hand_combat",
            charset="utf8mb4"
        )
        self.load_trainers()
        
        exit_button = self.exitButton
        if exit_button:
            exit_button.clicked.connect(self.confirm_exit)

        self.tableWidget_tab3.doubleClicked.connect(self.on_trainer_double_click)

        self.addbutton_tab2.clicked.connect(self.open_create_tren_dialog)
        self.izmenbutton_tab2.clicked.connect(self.open_create_tren_dialog)
        self.delbutton_tab2.clicked.connect(self.del_tren_dialog)

        self.addbutton_tab3.clicked.connect(self.create_coach_dialog)
        self.izmenbutton_tab3.clicked.connect(self.edit_coach)
        self.delbutton_tab3.clicked.connect(self.del_coach_dialog)

        self.addbutton_tab4.clicked.connect(self.create_sportman_dialog)
        self.izmenbutton_tab4.clicked.connect(self.create_sportman_dialog)
        self.delbutton_tab4.clicked.connect(self.del_sportman_dialog)

        self.addbutton_tab5.clicked.connect(self.create_gruppa_dialog)
        self.izmenbutton_tab5.clicked.connect(self.create_gruppa_dialog)
        self.delbutton_tab5.clicked.connect(self.del_gruppa_dialog)

        self.clearbutton_tab6.clicked.connect(self.del_otchet_dialog)

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
        create_coach_dialog = CreateCoachDialog(self.db_manager, self)
        if create_coach_dialog.exec_():
            self.load_trainers()

    def load_trainers(self):
        try:
            connection = connect_to_db()
            if not connection:
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных!")
                return

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = "SELECT Фамилия, Имя, Отчество, Доп_информация FROM Тренера"
                cursor.execute(query)
                trainers = cursor.fetchall()

            # Очищаем таблицу
            self.tableWidget_tab3.clearContents()
            self.tableWidget_tab3.setRowCount(len(trainers))
            self.tableWidget_tab3.setColumnCount(4)
            self.tableWidget_tab3.setHorizontalHeaderLabels(['Фамилия', 'Имя', 'Отчество', 'Дополнительная информация'])

            self.tableWidget_tab3.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tableWidget_tab3.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.tableWidget_tab3.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.tableWidget_tab3.setColumnWidth(0, 160)
            self.tableWidget_tab3.setColumnWidth(1, 160)
            self.tableWidget_tab3.setColumnWidth(2, 160)
            self.tableWidget_tab3.setColumnWidth(3, 300)

            for row_index, trainer in enumerate(trainers):
                self.tableWidget_tab3.setItem(row_index, 1, QTableWidgetItem(trainer['Фамилия']))
                self.tableWidget_tab3.setItem(row_index, 0, QTableWidgetItem(trainer['Имя']))
                self.tableWidget_tab3.setItem(row_index, 2, QTableWidgetItem(trainer['Отчество']))
                self.tableWidget_tab3.setItem(row_index, 3, QTableWidgetItem(trainer['Доп_информация']))

        except pymysql.Error as e:
            QMessageBox.critical(self, "Ошибка загрузки данных", f"Ошибка при обращении к базе данных: {e}")
        finally:
            if connection:
                connection.close()

    def on_trainer_double_click(self, index):
        row = index.row()

        # Извлекаем данные из выбранной строки
        surname = self.tableWidget_tab3.item(row, 1).text()
        name = self.tableWidget_tab3.item(row, 0).text()
        patronymic = self.tableWidget_tab3.item(row, 2).text()
        info = self.tableWidget_tab3.item(row, 3).text()

        # Открываем диалоговое окно для просмотра тренера
        create_coach_dialog = CreateCoachDialog(self.db_manager, self, view_mode=True)
        create_coach_dialog.surname_coach.setText(surname)
        create_coach_dialog.name_coach.setText(name)
        create_coach_dialog.otchestvo_coach.setText(patronymic)
        create_coach_dialog.dopinfo_coach.setPlainText(info)
        create_coach_dialog.exec_()

    def edit_coach(self):
        self.open_edit_coach_dialog()

    def open_edit_coach_dialog(self):
        selected_row = self.tableWidget_tab3.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите тренера для редактирования!")
            return

        surname = self.tableWidget_tab3.item(selected_row, 1).text()
        name = self.tableWidget_tab3.item(selected_row, 0).text()
        patronymic = self.tableWidget_tab3.item(selected_row, 2).text()
        info = self.tableWidget_tab3.item(selected_row, 3).text()

        edit_dialog = EditCoachDialog(self.db_manager, self)
        edit_dialog.set_coach_data(self.get_coach_id(surname, name, patronymic), surname, name, patronymic, info)
        edit_dialog.exec_()
        if edit_dialog.result():
            self.load_trainers()

    def get_coach_id(self, surname, name, patronymic):
        coach_id_query = "SELECT id_Тренера FROM Тренера WHERE Фамилия = %s AND Имя = %s AND Отчество = %s"
        result = self.db_manager.execute_query(coach_id_query, (surname, name, patronymic), fetch=True)
        if result:
            return result[0]['id_Тренера']
        return None
    
    def del_coach(self):
        # Получаем ID тренера из текущего выбранного элемента таблицы
        selected_row = self.tableWidget_tab3.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите тренера для удаления!")
            return
        else:
            surname = self.tableWidget_tab3.item(selected_row, 1).text()
            name = self.tableWidget_tab3.item(selected_row, 0).text()

            query = "DELETE FROM Тренера WHERE Фамилия = %s AND Имя = %s"
            params = (surname, name)
            self.db_manager.execute_query(query, params)

            # Обновляем таблицу после удаления
            self.load_trainers()

    def del_coach_dialog(self):
        del_coach = QDialog(self)
        uic.loadUi('forms/delcoach.ui', del_coach)
        yes_button = del_coach.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_coach.findChild(QtWidgets.QPushButton, "pushButton")
        if yes_button:
            yes_button.clicked.connect(lambda: (self.del_coach(), del_coach.close()))
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