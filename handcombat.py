import sys
import pymysql
import os 
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import QRegExp, QDate, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QPushButton, QTableWidgetItem, QHeaderView, QTableWidget
from database import DatabaseManager
from newmainwindow import Ui_Mainwindow
from createtren import Ui_Createtren
from create_sportman import Ui_SportMan
from create_gruppa import Ui_CreateGruppa
from create_coach import Ui_CreateCoach
from edit_coach import Ui_EditCoach
from edit_sportman import Ui_EditSportman

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

class CreateSportMan(QDialog, Ui_SportMan):
    def __init__(self, db_manager, view_mode, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db_manager = db_manager
        self.view_mode = view_mode
        
        self.setup_widgets()
        self.load_groups()
        
        self.addbutton_sportman.clicked.connect(self.add_sportman_to_db)
        self.cancelbutton_sportman.clicked.connect(self.reject)

    def load_groups(self):
        try:
            query = """
            SELECT г.id_Группы, г.Название, CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) as Тренер
            FROM Группы г
            JOIN Тренера т ON г.id_Тренера = т.id_Тренера
            """
            groups = self.db_manager.execute_query(query, fetch=True)
            
            self.grupaBox_sportman.clear()
            self.grupaBox_sportman.addItem("Выберите группу")
            
            self.group_ids = {}
            for group in groups:
                display_text = f"{group['Название']} - {group['Тренер']}"
                self.grupaBox_sportman.addItem(display_text)
                self.group_ids[display_text] = group['id_Группы']
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список групп: {e}")

    def setup_widgets(self):
        self.sportrazrBox.addItem("")
        self.sportrazrBox.addItems([
            "3ий юношеский", "2ой юношеский", "1ый юношеский",
            "3ий спортивный", "2ой спортивный", "1ый спортивный",
            "КМС", "МС", "МСМК", "ЗМС"
        ])

        self.datebirth_sportman.setCalendarPopup(True)

    def add_sportman_to_db(self):
        name = self.name_sportman.text().strip()
        surname = self.surname_sportman.text().strip()
        otchestvo = self.otchestvo_sportman.text().strip()
        grupa = self.grupaBox_sportman.currentText().strip()
        datebirth = self.datebirth_sportman.date().toString("yyyy-MM-dd")
        sportrazr = self.sportrazrBox.currentText().strip()

        if not all([surname, name]) or grupa == "Выберите группу":
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
            return

        if sportrazr == "":
            QMessageBox.warning(self, "Ошибка", "Выберите спортивный разряд!")
            return

        try:
            group_id = self.group_ids[grupa]
            query = """
            INSERT INTO Спортсмены (Фамилия, Имя, Отчество, id_Группы, Дата_рождения, Спортивный_разряд)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db_manager.execute_query(query, (name, surname, otchestvo, group_id, datebirth, sportrazr))
            
            if self.parent() and hasattr(self.parent(), 'load_sportsmans'):
                self.parent().load_sportsmans()
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить спортсмена: {e}")

class EditSportMan(QDialog, Ui_EditSportman):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db_manager = db_manager
        self.current_sportsman_id = None
        
        # Setup widgets and connections
        self.setup_widgets()
        self.load_groups()
        
        self.addbutton_sportman.clicked.connect(self.save_sportsman_changes)
        self.cancelbutton_sportman.clicked.connect(self.reject)

    def setup_widgets(self):
        self.sportrazrBox.addItem("")
        self.sportrazrBox.addItems([
            "3ий юношеский", "2ой юношеский", "1ый юношеский",
            "3ий спортивный", "2ой спортивный", "1ый спортивный",
            "КМС", "МС", "МСМК", "ЗМС"
        ])
        self.datebirth_sportman.setCalendarPopup(True)

    def load_groups(self):
        try:
            query = """
            SELECT г.id_Группы, г.Название, CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) as Тренер
            FROM Группы г
            JOIN Тренера т ON г.id_Тренера = т.id_Тренера
            """
            groups = self.db_manager.execute_query(query, fetch=True)
            
            self.grupaBox_sportman.clear()
            self.grupaBox_sportman.addItem("Выберите группу")
            
            self.group_ids = {}
            for group in groups:
                display_text = f"{group['Название']} - {group['Тренер']}"
                self.grupaBox_sportman.addItem(display_text)
                self.group_ids[display_text] = group['id_Группы']
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список групп: {e}")

    def set_sportsman_data(self, sportsman_id, surname, name, patronymic, group, birth_date, rank):
        self.current_sportsman_id = sportsman_id
        self.surname_sportman.setText(surname)
        self.name_sportman.setText(name)
        self.otchestvo_sportman.setText(patronymic)
        
        # Find and set the correct group in combobox
        index = self.grupaBox_sportman.findText(group, Qt.MatchContains)
        if index >= 0:
            self.grupaBox_sportman.setCurrentIndex(index)
            
        qdate = QDate.fromString(birth_date, "dd.MM.yyyy")
        if qdate.isValid():
            self.datebirth_sportman.setDate(qdate)
        
        # Set sport rank
        index = self.sportrazrBox.findText(rank)
        if index >= 0:
            self.sportrazrBox.setCurrentIndex(index)

    def save_sportsman_changes(self):
        new_name = self.surname_sportman.text().strip()
        new_surname = self.name_sportman.text().strip()
        new_patronymic = self.otchestvo_sportman.text().strip()
        new_group = self.grupaBox_sportman.currentText()
        new_birth_date = self.datebirth_sportman.date().toString("yyyy-MM-dd")
        new_rank = self.sportrazrBox.currentText()

        if not all([new_name, new_surname]) or new_group == "Выберите группу":
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
            return

        if new_rank == "":
            QMessageBox.warning(self, "Ошибка", "Выберите спортивный разряд!")
            return

        try:
            group_id = self.group_ids[new_group]
            update_query = """
            UPDATE Спортсмены 
            SET Фамилия = %s, Имя = %s, Отчество = %s, 
                id_Группы = %s, Дата_рождения = %s, Спортивный_разряд = %s
            WHERE id_Спортсмена = %s
            """
            params = (new_name, new_surname, new_patronymic, 
                     group_id, new_birth_date, new_rank, 
                     self.current_sportsman_id)
            
            self.db_manager.execute_query(update_query, params)
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные спортсмена: {e}")

class CreateGruppaDialog(QDialog, Ui_CreateGruppa):
    def __init__(self, db_manager, parent=None, view_mode=False):
        super().__init__(parent)
        self.setupUi(self)
        self.db_manager = db_manager
        self.view_mode = view_mode
        
        self.setup_widgets()
        
        self.addbutton_grupa.clicked.connect(self.add_group_to_db)
        self.cancelbutton_grupa.clicked.connect(self.reject)

        if self.view_mode:
            self.name_grupa.setReadOnly(True)
            self.comboBox_trener.setEnabled(False)
            self.addbutton_grupa.setEnabled(False)

    def setup_widgets(self):
        self.load_trainers()

    def load_trainers(self):
        try:
            query = "SELECT id_Тренера, CONCAT(Фамилия, ' ', Имя, ' ', Отчество) as ФИО FROM Тренера"
            trainers = self.db_manager.execute_query(query, fetch=True)
            
            self.comboBox_trener.clear()
            self.comboBox_trener.addItem("Выберите тренера")
            
            self.trainer_ids = {}
            for trainer in trainers:
                self.comboBox_trener.addItem(trainer['ФИО'])
                self.trainer_ids[trainer['ФИО']] = trainer['id_Тренера']
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список тренеров: {e}")

    def add_group_to_db(self):
        name = self.name_grupa.text().strip()
        trainer = self.comboBox_trener.currentText()

        if not name or trainer == "Выберите тренера":
            QMessageBox.warning(self, "Ошибка", "Заполните название группы и выберите тренера!")
            return

        try:
            # Проверяем существование такой же группы с тем же тренером
            check_query = """
            SELECT COUNT(*) as count 
            FROM Группы г 
            JOIN Тренера т ON г.id_Тренера = т.id_Тренера 
            WHERE г.Название = %s AND CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) = %s
            """
            result = self.db_manager.execute_query(check_query, (name, trainer), fetch=True)
            
            if result[0]['count'] > 0:
                QMessageBox.warning(self, "Ошибка", "Группа с таким названием и тренером уже существует!")
                return

            # Если группа уникальная - создаём её
            trainer_id = self.trainer_ids[trainer]
            query = "INSERT INTO Группы (Название, id_Тренера) VALUES (%s, %s)"
            self.db_manager.execute_query(query, (name, trainer_id))
            
            self.name_grupa.clear()
            self.comboBox_trener.setCurrentIndex(0)
            
            if self.parent() and hasattr(self.parent(), 'load_groups'):
                self.parent().load_groups()
                
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить группу: {e}")

class EditGruppaDialog(QDialog, Ui_CreateGruppa):
    def __init__(self, db_manager, parent=None, view_mode=False):
        super().__init__(parent)
        self.setupUi(self)
        self.db_manager = db_manager
        self.view_mode = view_mode
        self.current_group_id = None
        
        # Меняем текст кнопки на "Сохранить"
        self.addbutton_grupa.setText("Сохранить")
        
        self.addbutton_grupa.clicked.connect(self.save_group_changes)
        self.cancelbutton_grupa.clicked.connect(self.reject)
        
        if self.view_mode:
            self.name_grupa.setReadOnly(True)
            self.comboBox_trener.setEnabled(False)
            self.addbutton_grupa.setEnabled(False)
        
        self.setup_widgets()

    def setup_widgets(self):
        self.load_trainers()

    def load_trainers(self):
        try:
            query = "SELECT id_Тренера, CONCAT(Фамилия, ' ', Имя, ' ', Отчество) as ФИО FROM Тренера"
            trainers = self.db_manager.execute_query(query, fetch=True)
            
            self.comboBox_trener.clear()
            self.comboBox_trener.addItem("Выберите тренера")
            
            self.trainer_ids = {}
            for trainer in trainers:
                self.comboBox_trener.addItem(trainer['ФИО'])
                self.trainer_ids[trainer['ФИО']] = trainer['id_Тренера']
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список тренеров: {e}")

    def set_group_data(self, group_id, name, trainer):
        self.current_group_id = group_id
        self.name_grupa.setText(name)
        index = self.comboBox_trener.findText(trainer)
        if index >= 0:
            self.comboBox_trener.setCurrentIndex(index)

    def save_group_changes(self):
        new_name = self.name_grupa.text().strip()
        new_trainer = self.comboBox_trener.currentText()

        if not new_name or new_trainer == "Выберите тренера":
            QMessageBox.warning(self, "Ошибка", "Заполните название группы и выберите тренера!")
            return

        try:
            # Проверка на существование такой же группы
            check_query = """
            SELECT COUNT(*) as count 
            FROM Группы г 
            JOIN Тренера т ON г.id_Тренера = т.id_Тренера 
            WHERE г.Название = %s AND CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) = %s
            AND г.id_Группы != %s
            """
            result = self.db_manager.execute_query(check_query, (new_name, new_trainer, self.current_group_id), fetch=True)
            
            if result[0]['count'] > 0:
                QMessageBox.warning(self, "Ошибка", "Группа с таким названием и тренером уже существует!")
                return

            trainer_id = self.trainer_ids[new_trainer]
            update_query = """
            UPDATE Группы SET Название = %s, id_Тренера = %s 
            WHERE id_Группы = %s
            """
            self.db_manager.execute_query(update_query, (new_name, trainer_id, self.current_group_id))
            
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные группы: {e}")

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
        self.load_groups()
        self.load_sportmen()
        
        self.sport_ranks_order = {
                "3ий юношеский": 1,
                "2ой юношеский": 2,
                "1ый юношеский": 3,
                "3ий спортивный": 4,
                "2ой спортивный": 5,
                "1ый спортивный": 6,
                "КМС": 7,
                "МС": 8,
                "МСМК": 9,
                "ЗМС": 10
            }
        self.rank_sort_order = Qt.AscendingOrder

        exit_button = self.exitButton
        if exit_button:
            exit_button.clicked.connect(self.confirm_exit)

        self.tableWidget_tab3.doubleClicked.connect(self.on_trainer_double_click)
        self.tableWidget_tab5.doubleClicked.connect(self.on_group_double_click)

        self.tableWidget_tab4.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        self.date_sort_order = Qt.AscendingOrder  # Добавляем переменную для отслеживания порядка сортировки

        self.addbutton_tab2.clicked.connect(self.open_create_tren_dialog)
        self.izmenbutton_tab2.clicked.connect(self.open_create_tren_dialog)
        self.delbutton_tab2.clicked.connect(self.del_tren_dialog)

        self.addbutton_tab3.clicked.connect(self.create_coach_dialog)
        self.izmenbutton_tab3.clicked.connect(self.edit_coach)
        self.delbutton_tab3.clicked.connect(self.del_coach_dialog)

        self.addbutton_tab4.clicked.connect(self.create_sportman_dialog)
        self.izmenbutton_tab4.clicked.connect(self.edit_sportsman)
        self.delbutton_tab4.clicked.connect(self.del_sportman_dialog)

        self.addbutton_tab5.clicked.connect(self.create_gruppa_dialog)
        self.izmenbutton_tab5.clicked.connect(self.edit_group)
        self.delbutton_tab5.clicked.connect(self.delete_group)

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
            self.tableWidget_tab3.setColumnWidth(0, 180)
            self.tableWidget_tab3.setColumnWidth(1, 180)
            self.tableWidget_tab3.setColumnWidth(2, 180)
            self.tableWidget_tab3.setColumnWidth(3, 300)

            self.tableWidget_tab3.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows) 
            self.tableWidget_tab3.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

            self.tableWidget_tab3.setColumnHidden(3, True)

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
        create_sportman_dialog = CreateSportMan(self.db_manager, self)
        if create_sportman_dialog.exec_():
            self.load_sportmen()

    def edit_sportsman(self):
        selected_row = self.tableWidget_tab4.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите спортсмена для редактирования!")
            return

        # Get sportsman data from the table
        surname = self.tableWidget_tab4.item(selected_row, 1).text()
        name = self.tableWidget_tab4.item(selected_row, 0).text()
        patronymic = self.tableWidget_tab4.item(selected_row, 2).text()
        group = self.tableWidget_tab4.item(selected_row, 3).text()
        birth_date = self.tableWidget_tab4.item(selected_row, 4).text()
        rank = self.tableWidget_tab4.item(selected_row, 5).text()

        # Get sportsman ID from database
        query = """
        SELECT id_Спортсмена 
        FROM Спортсмены 
        WHERE Фамилия = %s AND Имя = %s AND Отчество = %s
        """
        result = self.db_manager.execute_query(query, (surname, name, patronymic), fetch=True)
        if not result:
            QMessageBox.warning(self, "Ошибка", "Спортсмен не найден в базе данных!")
            return

        sportsman_id = result[0]['id_Спортсмена']

        # Create and show edit dialog
        edit_dialog = EditSportMan(self.db_manager, self)
        edit_dialog.set_sportsman_data(sportsman_id, surname, name, patronymic, 
                                    group, birth_date, rank)
        
        if edit_dialog.exec_():
            self.load_sportmen()

    def load_sportmen(self):
        try:
            connection = connect_to_db()
            if not connection:
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных!")
                return

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT с.Фамилия, с.Имя, с.Отчество, г.Название as Группа, 
                    с.Дата_рождения, с.Спортивный_разряд 
                FROM Спортсмены с
                JOIN Группы г ON с.id_Группы = г.id_Группы
                """
                cursor.execute(query)
                sportmen = cursor.fetchall()

            # Очищаем таблицу
            self.tableWidget_tab4.clearContents()
            self.tableWidget_tab4.setRowCount(len(sportmen))
            self.tableWidget_tab4.setColumnCount(6)
            self.tableWidget_tab4.setHorizontalHeaderLabels([
                'Фамилия', 'Имя', 'Отчество', 'Группа', 'Дата рождения', 'Разряд'
            ])

            self.tableWidget_tab4.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tableWidget_tab4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableWidget_tab4.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows) 
            self.tableWidget_tab4.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

            for row_index, sportman in enumerate(sportmen):
                self.tableWidget_tab4.setItem(row_index, 1, QTableWidgetItem(sportman['Фамилия']))
                self.tableWidget_tab4.setItem(row_index, 0, QTableWidgetItem(sportman['Имя']))
                self.tableWidget_tab4.setItem(row_index, 2, QTableWidgetItem(sportman['Отчество']))
                self.tableWidget_tab4.setItem(row_index, 3, QTableWidgetItem(sportman['Группа']))
                self.tableWidget_tab4.setItem(row_index, 4, QTableWidgetItem(sportman['Дата_рождения'].strftime('%d.%m.%Y')))
                self.tableWidget_tab4.setItem(row_index, 5, QTableWidgetItem(sportman['Спортивный_разряд']))

        except pymysql.Error as e:
            QMessageBox.critical(self, "Ошибка загрузки данных", f"Ошибка при обращении к базе данных: {e}")
        finally:
            if connection:
                connection.close()

    def on_sportman_double_click(self, index):
        row = index.row()

        # Извлекаем данные из выбранной строки
        surname = self.tableWidget_tab4.item(row, 0).text()
        name = self.tableWidget_tab4.item(row, 1).text()
        patronymic = self.tableWidget_tab4.item(row, 2).text()
        grupa = self.tableWidget_tab4.item(row, 3).text()
        datebirth = self.tableWidget_tab4.item(row, 4).text()
        sportrazr = self.tableWidget_tab4.item(row, 5).text()

        create_sportman_dialog = CreateSportMan(self.db_manager, self, view_mode=True)
        create_sportman_dialog.surname_sportman.setText(surname)
        create_sportman_dialog.name_sportman.setText(name)
        create_sportman_dialog.otchestvo_sportman.setText(patronymic)
        create_sportman_dialog.grupaBox_sportman.setCurrentText(grupa)
        create_sportman_dialog.datebirth_sportman.setDate(QDate.fromString(datebirth, "yyyy-MM-dd"))
        create_sportman_dialog.sportrazrBox.setCurrentText(sportrazr)
        create_sportman_dialog.exec_()

    def on_header_clicked(self, logical_index):
        if logical_index == 4:  # Индекс колонки с датой рождения
            self.tableWidget_tab4.sortItems(4, self.date_sort_order)
            # Меняем порядок сортировки на противоположный для следующего клика
            self.date_sort_order = Qt.DescendingOrder if self.date_sort_order == Qt.AscendingOrder else Qt.AscendingOrder
        elif logical_index == 5:  # Спортивный разряд
            self.sort_by_rank()
    
    def sort_by_rank(self):
        rows_data = []
        for row in range(self.tableWidget_tab4.rowCount()):
            row_data = []
            for col in range(self.tableWidget_tab4.columnCount()):
                item = self.tableWidget_tab4.item(row, col)
                row_data.append(item.text() if item else "")
            rows_data.append(row_data)
        
        # Сортировка по рангу
        rows_data.sort(
            key=lambda x: self.sport_ranks_order.get(x[5], 0),
            reverse=self.rank_sort_order == Qt.DescendingOrder
        )
        
        # Обновление таблицы
        for row, data in enumerate(rows_data):
            for col, value in enumerate(data):
                self.tableWidget_tab4.setItem(row, col, QTableWidgetItem(value))
        
        self.rank_sort_order = Qt.DescendingOrder if self.rank_sort_order == Qt.AscendingOrder else Qt.AscendingOrder

    def del_sportman(self):
        selected_row = self.tableWidget_tab4.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите спортсмена для удаления!")
            return

        surname = self.tableWidget_tab4.item(selected_row, 1).text()
        name = self.tableWidget_tab4.item(selected_row, 0).text()
        patronymic = self.tableWidget_tab4.item(selected_row, 2).text()

        try:
            query = """
            DELETE FROM Спортсмены 
            WHERE Фамилия = %s AND Имя = %s AND Отчество = %s
            """
            self.db_manager.execute_query(query, (surname, name, patronymic))
            self.load_sportmen()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить спортсмена: {e}")

    def del_sportman_dialog(self):
        del_sportman = QDialog(self)
        uic.loadUi('forms/delsportman.ui', del_sportman)
        yes_button = del_sportman.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_sportman.findChild(QtWidgets.QPushButton, "pushButton")
        
        if yes_button:
            yes_button.clicked.connect(lambda: (self.del_sportman(), del_sportman.close()))
        if no_button:
            no_button.clicked.connect(del_sportman.close)
        
        del_sportman.exec_()

    def create_gruppa_dialog(self):
        create_gruppa = CreateGruppaDialog(db_manager=self.db_manager, parent=self)
        create_gruppa.exec_()

    def load_groups(self):
        try:
            query = """
            SELECT г.id_Группы, г.Название, 
                CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) as Тренер
            FROM Группы г
            JOIN Тренера т ON г.id_Тренера = т.id_Тренера
            """
            groups = self.db_manager.execute_query(query, fetch=True)
            
            # Configure table
            self.tableWidget_tab5.clearContents()
            self.tableWidget_tab5.setRowCount(len(groups))
            self.tableWidget_tab5.setColumnCount(3)
            self.tableWidget_tab5.setHorizontalHeaderLabels(['ID', 'Название группы', 'Тренер'])
            self.tableWidget_tab5.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tableWidget_tab5.setColumnWidth(1, 180)
            self.tableWidget_tab5.setColumnWidth(2, 300)

            self.tableWidget_tab5.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows) 
            self.tableWidget_tab5.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            
            # Fill table
            for row, group in enumerate(groups):
                self.tableWidget_tab5.setItem(row, 0, QTableWidgetItem(str(group['id_Группы'])))
                self.tableWidget_tab5.setItem(row, 1, QTableWidgetItem(group['Название']))
                self.tableWidget_tab5.setItem(row, 2, QTableWidgetItem(group['Тренер']))
                
            # Hide ID column
            self.tableWidget_tab5.setColumnHidden(0, True)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить группы: {e}")

    def on_group_double_click(self, index):
        row = index.row()
        
        # Получаем данные из выбранной строки
        group_name = self.tableWidget_tab5.item(row, 1).text()
        trainer_name = self.tableWidget_tab5.item(row, 2).text()
        
        # Создаём диалог в режиме просмотра
        view_dialog = CreateGruppaDialog(self.db_manager, self, view_mode=True)
        
        # Заполняем поля данными
        view_dialog.name_grupa.setText(group_name)
        view_dialog.comboBox_trener.addItem(trainer_name)
        view_dialog.comboBox_trener.setCurrentText(trainer_name)
        
        # Делаем поля только для чтения
        view_dialog.name_grupa.setReadOnly(True)
        view_dialog.comboBox_trener.setEnabled(False)
        view_dialog.addbutton_grupa.setEnabled(False)
        
        view_dialog.exec_()

    def edit_group(self):
        selected_row = self.tableWidget_tab5.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для редактирования!")
            return

        group_id = self.tableWidget_tab5.item(selected_row, 0).text()
        group_name = self.tableWidget_tab5.item(selected_row, 1).text()
        trainer_name = self.tableWidget_tab5.item(selected_row, 2).text()

        edit_dialog = EditGruppaDialog(self.db_manager, self)
        edit_dialog.set_group_data(group_id, group_name, trainer_name)
        
        if edit_dialog.exec_():
            self.load_groups()

    def delete_group(self):
        selected_row = self.tableWidget_tab5.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для удаления!")
            return
            
        group_id = self.tableWidget_tab5.item(selected_row, 0).text()
        group_name = self.tableWidget_tab5.item(selected_row, 1).text()
        
        reply = QMessageBox.question(self, 'Подтверждение', 
                                f'Вы уверены, что хотите удалить группу "{group_name}"?',
                                QMessageBox.Yes | QMessageBox.No)
                                
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM Группы WHERE id_Группы = %s"
                self.db_manager.execute_query(query, (group_id,))
                self.load_groups()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить группу: {e}")

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