import sys, os
import pymysql
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import QRegExp, QDate, Qt
from PyQt5.QtGui import QRegExpValidator, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QTableWidgetItem, QHeaderView, QTableWidget, QAbstractItemView, QCheckBox, QWidget, QHBoxLayout, QCalendarWidget
from database import DatabaseManager
from newmainwindow import Ui_Mainwindow
from createtren import Ui_Createtren
from edit_tren import Ui_EditTren
from create_sportman import Ui_SportMan
from create_gruppa import Ui_CreateGruppa
from create_coach import Ui_CreateCoach
from edit_coach import Ui_EditCoach
from edit_sportman import Ui_EditSportman

ENCRYPTION_KEY = b't3KB2lvpMsmVMH-uRPrLwp_mfIhbQwGsOx3oANi3aiY='

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
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        uic.loadUi('forms/loginform.ui', self)
        
        self.db_manager = db_manager
        
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
        
        try:
            query = "SELECT * FROM admin_user"
            results = self.db_manager.execute_query(query, fetch=True)
            result = results[0]
            
            # Decrypt stored credentials
            stored_login = self.db_manager.crypto.decrypt(result['login'])
            stored_password = self.db_manager.crypto.decrypt(result['password'])
            
            if username == stored_login.decode() and password == stored_password.decode():
                print("Успешная авторизация!")
                self.accept()
            else:
                print("Неверные учетные данные")
                self.show_error_dialog()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка аутентификации: {e}")

    def logout(self):
        self.logout_dialog = QDialog(self)
        uic.loadUi('forms/logoutsystem.ui', self.logout_dialog)
        
        da_button = self.logout_dialog.findChild(QtWidgets.QPushButton, "pushButton_2")
        net_button = self.logout_dialog.findChild(QtWidgets.QPushButton, "pushButton")
        
        if da_button:
            da_button.clicked.connect(self.exit_system)
            self.logout_dialog.close()
        if net_button:
            net_button.clicked.connect(self.logout_dialog.close)
            
        self.logout_dialog.exec_()

    def show_error_dialog(self):
        error_dialog = QDialog(self)
        uic.loadUi('forms/errorlogin.ui', error_dialog)
        
        ok_button = error_dialog.findChild(QtWidgets.QPushButton, "pushButton")
        if ok_button:
            ok_button.clicked.connect(error_dialog.close)
            
        error_dialog.exec_()

    def exit_system(self):
        sys.exit()

class CreateTren(QDialog, Ui_Createtren):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db_manager = db_manager

        # Настраиваем виджеты
        self.setup_widgets()
        
        # Загружаем данные в комбобоксы
        self.load_trainers()
        self.load_groups()
        
        # Подключаем сигналы
        self.addbutton_soztren.clicked.connect(self.add_training)
        self.cancelbutton_soztren.clicked.connect(self.reject)
    
    def refresh_groups(self):
        self.load_groups()
        if hasattr(self, 'trenerBox_soztren') and self.trenerBox_soztren.currentText() != "Выберите тренера":
            self.update_groups_for_trainer(self.trenerBox_soztren.currentText())

    def setup_widgets(self):
        # Настройка QDateTimeEdit
        current_datetime = QtCore.QDateTime.currentDateTime()
        self.dateTimeEdit_soztren.setDateTime(current_datetime)
        self.dateTimeEdit_soztren.setMinimumDateTime(current_datetime)
        self.dateTimeEdit_soztren.setCalendarPopup(True)

    def load_trainers(self):
        query = """
        SELECT DISTINCT т.id_Тренера, CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) as ФИО 
        FROM Тренера т
        INNER JOIN Группы г ON т.id_Тренера = г.id_Тренера
        """
        trainers = self.db_manager.execute_query(query, fetch=True)
        
        self.trenerBox_soztren.clear()
        self.trenerBox_soztren.addItem("Выберите тренера")
        
        self.trainer_ids = {}
        for trainer in trainers:
            self.trenerBox_soztren.addItem(trainer['ФИО'])
            self.trainer_ids[trainer['ФИО']] = trainer['id_Тренера']

        # Connect signal to slot
        self.trenerBox_soztren.currentTextChanged.connect(self.update_groups_for_trainer)

    def update_groups_for_trainer(self, trainer_name):
        if not trainer_name or trainer_name == "Выберите тренера":
            self.grupaBox_soztren.clear()
            return
        
        trainer_id = self.trainer_ids[trainer_name]
        query = """
        SELECT id_Группы, Название
        FROM Группы
        WHERE id_Тренера = %s
        """
        groups = self.db_manager.execute_query(query, (trainer_id,), fetch=True)
        
        self.grupaBox_soztren.clear()
        self.group_ids = {}
        for group in groups:
            self.grupaBox_soztren.addItem(group['Название'])
            self.group_ids[group['Название']] = group['id_Группы']

    def load_groups(self):
        try:
            query = """
            SELECT г.id_Группы, г.Название, CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) as Тренер
            FROM Группы г
            JOIN Тренера т ON г.id_Тренера = т.id_Тренера
            """
            groups = self.db_manager.execute_query(query, fetch=True)
            
            self.grupaBox_soztren.clear()
            self.grupaBox_soztren.addItem("Выберите группу")
            
            self.group_ids = {}
            for group in groups:
                display_text = f"{group['Название']}"
                self.grupaBox_soztren.addItem(display_text)
                self.group_ids[display_text] = group['id_Группы']
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список групп: {e}")

    def add_training(self):
        name = self.name_tren.text().strip()
        trainer = self.trenerBox_soztren.currentText()
        group = self.grupaBox_soztren.currentText()
        datetime = self.dateTimeEdit_soztren.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        if not name or trainer == "Выберите тренера" or not group:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        try:
            trainer_id = self.trainer_ids[trainer]
            group_id = self.group_ids[group]
            
            # Создаем тренировку
            query = """
            INSERT INTO Расписание_тренировок (Название, id_Тренера, id_Группы, Дата_время)
            VALUES (%s, %s, %s, %s)
            """
            self.db_manager.execute_query(query, (name, trainer_id, group_id, datetime))

            # Получаем всех спортсменов группы
            query_athletes = """
            SELECT id_Спортсмена 
            FROM Спортсмены 
            WHERE id_Группы = %s
            """
            athletes = self.db_manager.execute_query(query_athletes, (group_id,), fetch=True)

            # Создаем записи с нулевыми отметками для всех спортсменов
            insert_attendance = """
            INSERT INTO Посещаемость (id_Спортсмена, id_Группы, Дата_время, Отметка)
            VALUES (%s, %s, %s, 0)
            """
            for athlete in athletes:
                self.db_manager.execute_query(
                    insert_attendance, 
                    (athlete['id_Спортсмена'], group_id, datetime)
                )

            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать тренировку: {e}")

class EditTren(QDialog, Ui_EditTren):
    def __init__(self, db_manager, parent=None, edit_mode=False):
        super().__init__(parent)
        self.setupUi(self)
        self.db_manager = db_manager
        self.edit_mode = edit_mode
        self.trainer_ids = {}
        self.group_ids = {}
        
        self.setup_widgets()
        self.load_trainers()
        self.load_groups()
        
        if edit_mode:
            self.addbutton_soztren.setText("Сохранить")
            self.addbutton_soztren.clicked.connect(self.update_training)
        else:
            self.addbutton_soztren.setVisible(True)
            self.name_tren.setEnabled(False)
            self.dateTimeEdit_soztren.setEnabled(False)
        
        self.cancelbutton_soztren.clicked.connect(self.reject)

    def setup_widgets(self):
        self.dateTimeEdit_soztren.setCalendarPopup(True)
        self.dateTimeEdit_soztren.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1)))

    def set_training_data(self, training_data):
        self.training_id = training_data['id_Тренировки']
        self.name_tren.setText(training_data['Название'])
        
        # Устанавливаем тренера и группу
        self.trenerBox_soztren.clear()
        self.trenerBox_soztren.addItem(training_data['Тренер'])
        
        self.grupaBox_soztren.clear()
        self.grupaBox_soztren.addItem(training_data['Группа'])
        
        # Устанавливаем дату и время
        if isinstance(training_data['Дата_время'], str):
            datetime_obj = QtCore.QDateTime.fromString(training_data['Дата_время'], 'yyyy-MM-dd HH:mm:ss')
        else:
            datetime_obj = QtCore.QDateTime.fromString(
                training_data['Дата_время'].strftime('%Y-%m-%d %H:%M:%S'),
                'yyyy-MM-dd HH:mm:ss'
            )
        self.dateTimeEdit_soztren.setDateTime(datetime_obj)

    def update_training(self):
        name = self.name_tren.text().strip()
        trainer = self.trenerBox_soztren.currentText()
        group = self.grupaBox_soztren.currentText()
        formatted_datetime = self.dateTimeEdit_soztren.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        if not name or not trainer or not group:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        try:
            trainer_id = self.trainer_ids[trainer]
            group_id = self.group_ids[group]
            
            query = """
            UPDATE Расписание_тренировок 
            SET Название = %s, id_Тренера = %s, id_Группы = %s, Дата_время = %s
            WHERE id_Тренировки = %s
            """
            self.db_manager.execute_query(query, (name, trainer_id, group_id, formatted_datetime, self.training_id))
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить тренировку: {e}")

    def load_trainers(self):
        query = """
        SELECT id_Тренера, CONCAT(Фамилия, ' ', Имя, ' ', Отчество) as ФИО 
        FROM Тренера
        """
        trainers = self.db_manager.execute_query(query, fetch=True)
        
        self.trainer_ids = {trainer['ФИО']: trainer['id_Тренера'] for trainer in trainers}

    def load_groups(self):
        query = """
        SELECT id_Группы, Название
        FROM Группы
        """
        groups = self.db_manager.execute_query(query, fetch=True)
        
        self.group_ids = {group['Название']: group['id_Группы'] for group in groups}

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
            self.grupaBox_sportman.addItem("Без группы")
            
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
        surname = self.name_sportman.text().strip()
        name = self.surname_sportman.text().strip()
        otchestvo = self.otchestvo_sportman.text().strip()
        grupa = self.grupaBox_sportman.currentText().strip()
        datebirth = self.datebirth_sportman.date().toString("yyyy-MM-dd")
        sportrazr = self.sportrazrBox.currentText().strip()

        if not all([surname, name]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
            return

        if sportrazr == "":
            QMessageBox.warning(self, "Ошибка", "Выберите спортивный разряд!")
            return

        try:
            group_id = None if grupa == "Без группы" else self.group_ids[grupa]
            
            query = """
            INSERT INTO Спортсмены (Фамилия, Имя, Отчество, id_Группы, Дата_рождения, Спортивный_разряд)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db_manager.execute_query(query, (surname, name, otchestvo, group_id, datebirth, sportrazr))
            
            if self.parent():
                if hasattr(self.parent(), 'load_sportsmans'):
                    self.parent().load_sportsmans()
                if hasattr(self.parent(), 'load_sportmen'):
                    self.parent().load_sportmen()
            
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
            self.grupaBox_sportman.addItem("Без группы")
            
            self.group_ids = {}
            for group in groups:
                display_text = f"{group['Название']} - {group['Тренер']}"
                self.grupaBox_sportman.addItem(display_text)
                self.group_ids[display_text] = group['id_Группы']
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список групп: {e}")

    def set_sportsman_data(self, sportsman_id, name, surname, patronymic, group, birth_date, rank):
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

        if not all([new_name, new_surname]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
            return

        if new_rank == "":
            QMessageBox.warning(self, "Ошибка", "Выберите спортивный разряд!")
            return

        try:
            # Handle "Без группы" case
            group_id = self.group_ids.get(new_group) if new_group != "Без группы" else None
            
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
        self.setup_table()

        search_style = """
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """

        self.search_sportsman = QtWidgets.QLineEdit(self)
        self.search_sportsman.setGeometry(QtCore.QRect(380, 115, 185, 30))
        self.search_sportsman.setPlaceholderText("Поиск спортсмена...")
        self.search_sportsman.textChanged.connect(self.search_sportsmen)
        self.search_sportsman.setMaxLength(20)
        self.search_sportsman.setStyleSheet(search_style)
        
        self.load_sportsmen()

        self.addbutton_grupa.clicked.connect(self.add_group_to_db)
        self.cancelbutton_grupa.clicked.connect(self.reject)

# Add search method
    def search_sportsmen(self):
        search_text = self.search_sportsman.text().lower()
        for row in range(self.tableWidget.rowCount()):
            show_row = False
            for col in range(1, self.tableWidget.columnCount()):  # Start from 1 to skip checkbox column
                item = self.tableWidget.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.tableWidget.setRowHidden(row, not show_row)

        if self.view_mode:
            self.name_grupa.setReadOnly(True)
            self.comboBox_trener.setEnabled(False)
            self.addbutton_grupa.setEnabled(False)

    def setup_widgets(self):
        self.load_trainers()

    def setup_table(self):
        self.tableWidget.setColumnCount(3)  # Добавляем столбец для чекбокса
        self.tableWidget.setHorizontalHeaderLabels([' ', 'ФИО', 'Дата рождения'])
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        
        self.tableWidget.setColumnWidth(0, 30)  # Ширина для чекбокса
        self.tableWidget.setColumnWidth(1, 365)
        self.tableWidget.setColumnWidth(2, 105)

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

    def load_sportsmen(self):
        try:
            all_sportsmen = []
            
            # Если есть ID группы (режим редактирования), загружаем её спортсменов
            if hasattr(self, 'group_id'):
                query_group = """
                SELECT CONCAT(Фамилия, ' ', Имя, ' ', Отчество) as ФИО, 
                    Дата_рождения, 
                    Фамилия, Имя, Отчество,
                    id_Спортсмена,
                    TRUE as in_group
                FROM Спортсмены
                WHERE id_Группы = %s
                """
                group_sportsmen = self.db_manager.execute_query(query_group, (self.group_id,), fetch=True)
                all_sportsmen.extend(group_sportsmen)

            # Загружаем спортсменов без группы
            query_free = """
            SELECT CONCAT(Фамилия, ' ', Имя, ' ', Отчество) as ФИО, 
                Дата_рождения, 
                Фамилия, Имя, Отчество,
                id_Спортсмена,
                FALSE as in_group
            FROM Спортсмены
            WHERE id_Группы IS NULL
            """
            free_sportsmen = self.db_manager.execute_query(query_free, fetch=True)
            all_sportsmen.extend(free_sportsmen)

            self.tableWidget.setRowCount(len(all_sportsmen))
            self.sportsmen_data = {}

            for row, sportsman in enumerate(all_sportsmen):
                # Добавляем чекбокс
                checkbox = QCheckBox()
                checkbox.setChecked(sportsman['in_group'])
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                self.tableWidget.setCellWidget(row, 0, checkbox_widget)

                self.tableWidget.setItem(row, 1, QTableWidgetItem(sportsman['ФИО']))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(sportsman['Дата_рождения'])))

                self.sportsmen_data[row] = {
                    'id': sportsman['id_Спортсмена'],
                    'Фамилия': sportsman['Фамилия'],
                    'Имя': sportsman['Имя'],
                    'Отчество': sportsman['Отчество']
                }

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список спортсменов: {e}")

    def add_group_to_db(self):
        name = self.name_grupa.text().strip()
        trainer = self.comboBox_trener.currentText()

        if not name or trainer == "Выберите тренера":
            QMessageBox.warning(self, "Ошибка", "Заполните название группы и выберите тренера!")
            return

        try:
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

            trainer_id = self.trainer_ids[trainer]
            query = "INSERT INTO Группы (Название, id_Тренера) VALUES (%s, %s)"
            self.db_manager.execute_query(query, (name, trainer_id))

            # Получаем ID созданной группы
            query = "SELECT id_Группы FROM Группы WHERE Название = %s AND id_Тренера = %s"
            result = self.db_manager.execute_query(query, (name, trainer_id), fetch=True)
            group_id = result[0]['id_Группы']

            # Добавляем выбранных спортсменов в группу
            for row in range(self.tableWidget.rowCount()):
                checkbox_widget = self.tableWidget.cellWidget(row, 0)
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    sportsman_id = self.sportsmen_data[row]['id']
                    update_query = "UPDATE Спортсмены SET id_Группы = %s WHERE id_Спортсмена = %s"
                    self.db_manager.execute_query(update_query, (group_id, sportsman_id))
            
            self.name_grupa.clear()
            self.comboBox_trener.setCurrentIndex(0)
            
            if self.parent():
                if hasattr(self.parent(), 'load_groups'):
                    self.parent().load_groups()
                if hasattr(self.parent(), 'load_sportmen'):
                    self.parent().load_sportmen()
            
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
        
        self.setup_widgets()
        self.setup_table()

        search_style = """
                    QLineEdit {
                        background-color: white;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 5px;
                    }
                """

        self.search_sportsman = QtWidgets.QLineEdit(self)
        self.search_sportsman.setGeometry(QtCore.QRect(380, 115, 185, 30))
        self.search_sportsman.setPlaceholderText("Поиск спортсмена...")
        self.search_sportsman.textChanged.connect(self.search_sportsmen)
        self.search_sportsman.setMaxLength(20)
        self.search_sportsman.setStyleSheet(search_style)

        self.addbutton_grupa.setText("Сохранить")
        self.addbutton_grupa.clicked.connect(self.save_group_changes)
        self.cancelbutton_grupa.clicked.connect(self.reject)

        if self.view_mode:
            self.name_grupa.setReadOnly(True)
            self.comboBox_trener.setEnabled(False)
            self.addbutton_grupa.setEnabled(False)
        
# Add search method
    def search_sportsmen(self):
        search_text = self.search_sportsman.text().lower()
        for row in range(self.tableWidget.rowCount()):
            show_row = False
            for col in range(1, self.tableWidget.columnCount()):  # Start from 1 to skip checkbox column
                item = self.tableWidget.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.tableWidget.setRowHidden(row, not show_row)
        
        self.setup_widgets()
        self.setup_table()

    def setup_widgets(self):
        self.load_trainers()

    def setup_table(self):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels([' ', 'ФИО', 'Дата рождения'])
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setSelectionMode(QTableWidget.NoSelection)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        
        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setColumnWidth(1, 365)
        self.tableWidget.setColumnWidth(2, 105)

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

    def load_sportsmen(self):
        try:
            if self.view_mode:
                # Загружаем только спортсменов текущей группы
                query = """
                SELECT CONCAT(Фамилия, ' ', Имя, ' ', Отчество) as ФИО, 
                    Дата_рождения, 
                    Фамилия, Имя, Отчество,
                    id_Спортсмена,
                    TRUE as in_group
                FROM Спортсмены
                WHERE id_Группы = %s
                """
                all_sportsmen = list(self.db_manager.execute_query(query, (self.current_group_id,), fetch=True))
            else:
                # Загружаем всех спортсменов (и группы, и без группы)
                query_group = """
                SELECT CONCAT(Фамилия, ' ', Имя, ' ', Отчество) as ФИО, 
                    Дата_рождения, 
                    Фамилия, Имя, Отчество,
                    id_Спортсмена,
                    TRUE as in_group
                FROM Спортсмены
                WHERE id_Группы = %s
                """
                group_sportsmen = list(self.db_manager.execute_query(query_group, (self.current_group_id,), fetch=True))

                query_free = """
                SELECT CONCAT(Фамилия, ' ', Имя, ' ', Отчество) as ФИО, 
                    Дата_рождения, 
                    Фамилия, Имя, Отчество,
                    id_Спортсмена,
                    FALSE as in_group
                FROM Спортсмены
                WHERE id_Группы IS NULL
                """
                free_sportsmen = list(self.db_manager.execute_query(query_free, fetch=True))
                all_sportsmen = group_sportsmen + free_sportsmen

            self.tableWidget.setRowCount(len(all_sportsmen))
            self.sportsmen_data = {}
            
            for row, sportsman in enumerate(all_sportsmen):
                checkbox = QCheckBox()
                checkbox.setChecked(sportsman['in_group'])
                if self.view_mode:
                    checkbox.setEnabled(False)
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                self.tableWidget.setCellWidget(row, 0, checkbox_widget)
                
                self.tableWidget.setItem(row, 1, QTableWidgetItem(sportsman['ФИО']))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(sportsman['Дата_рождения'])))
                
                self.sportsmen_data[row] = {
                    'id': sportsman['id_Спортсмена'],
                    'Фамилия': sportsman['Фамилия'],
                    'Имя': sportsman['Имя'],
                    'Отчество': sportsman['Отчество']
                }
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список спортсменов: {e}")

    def set_group_data(self, group_id, name, trainer):
        self.current_group_id = group_id
        self.name_grupa.setText(name)
        index = self.comboBox_trener.findText(trainer)
        if index >= 0:
            self.comboBox_trener.setCurrentIndex(index)
        self.load_sportsmen()

    def save_group_changes(self):
        new_name = self.name_grupa.text().strip()
        new_trainer = self.comboBox_trener.currentText()

        if not new_name or new_trainer == "Выберите тренера":
            QMessageBox.warning(self, "Ошибка", "Заполните название группы и выберите тренера!")
            return

        try:
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
            
            # Обновляем данные группы
            update_query = """
            UPDATE Группы SET Название = %s, id_Тренера = %s 
            WHERE id_Группы = %s
            """
            self.db_manager.execute_query(update_query, (new_name, trainer_id, self.current_group_id))

            # Обновляем состав группы
            for row in range(self.tableWidget.rowCount()):
                checkbox_widget = self.tableWidget.cellWidget(row, 0)
                checkbox = checkbox_widget.findChild(QCheckBox)
                sportsman_id = self.sportsmen_data[row]['id']
                
                if checkbox.isChecked():
                    update_query = "UPDATE Спортсмены SET id_Группы = %s WHERE id_Спортсмена = %s"
                    self.db_manager.execute_query(update_query, (self.current_group_id, sportsman_id))
                else:
                    update_query = "UPDATE Спортсмены SET id_Группы = NULL WHERE id_Спортсмена = %s"
                    self.db_manager.execute_query(update_query, (sportsman_id,))

            if self.parent():
                if hasattr(self.parent(), 'load_groups'):
                    self.parent().load_groups()
                if hasattr(self.parent(), 'load_sportmen'):
                    self.parent().load_sportmen()
                if hasattr(self.parent(), 'refresh_groups_combobox'):
                    self.parent().refresh_groups_combobox()
                if hasattr(self.parent(), 'refresh_groups_tab2'):
                    self.parent().refresh_groups_tab2()
            
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные группы: {e}")

class CreateCoachDialog(QDialog, Ui_CreateCoach):
    def __init__(self, db_manager, parent=None, view_mode=False):
        super().__init__(parent)
        self.setupUi(self)  # Задаём интерфейс через метод setupUi
        self.db_manager = db_manager
        self.view_mode = view_mode
                
        self.addbutton_coach.clicked.connect(self.add_coach_to_db)
        self.cancelbutton_coach.clicked.connect(self.reject)
        
        self.number_coach.setPlaceholderText("Номер телефона")
        self.number_coach.setInputMask("")

        self.number_coach.textEdited.connect(self.apply_input_mask)
        self.number_coach.cursorPositionChanged.connect(self.adjust_cursor_position)

    def apply_input_mask(self):
        # Если текст пустой, сбрасываем маску
        if not self.number_coach.text():
            self.number_coach.setInputMask("")
            self.number_coach.setPlaceholderText("Номер телефона")
        elif not self.number_coach.inputMask():
            self.number_coach.setInputMask('+7(999) 999-99-99')
            self.number_coach.setCursorPosition(4)

    def adjust_cursor_position(self):
        if self.number_coach.cursorPosition() < 3:
            self.number_coach.setCursorPosition(3)

        if self.view_mode:
            # Блокируем поля для редактирования и кнопку "Добавить"
            self.surname_coach.setReadOnly(True)
            self.name_coach.setReadOnly(True)
            self.otchestvo_coach.setReadOnly(True)
            self.dopinfo_coach.setReadOnly(True)
            self.number_coach.setReadOnly(True)

            self.add_button = self.findChild(QPushButton, "addbutton_coach")
            if self.add_button:
                self.add_button.setEnabled(False)  # Блокируем кнопку "Добавить"

    def add_coach_to_db(self):
        name = self.surname_coach.text().strip()
        surname = self.name_coach.text().strip()
        patronymic = self.otchestvo_coach.text().strip()
        info = self.dopinfo_coach.toPlainText().strip()
        number = ''.join(filter(str.isdigit, self.number_coach.text()))
        
        if self.number_coach.text().replace('(', '').replace(')', '').replace('-', '').replace(' ', '').strip() == '+7':
            number = ''  # Считаем поле пустым
        else:
            number = ''.join(filter(str.isdigit, self.number_coach.text()))
            if number:
                # Проверка на полноту номера (должно быть 11 цифр)
                if len(number) != 11:
                    QMessageBox.warning(self, "Ошибка", "Номер телефона введен не полностью!")
                    return False
                number = f'+7{number[1:]}' if number.startswith('7') else f'+7{number}'
            else:
                number = ''

        if not surname or not name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и Имя обязательны для заполнения!")
            return False

        # Проверка на дубликат ФИО
        check_name_query = """
        SELECT COUNT(*) as count FROM Тренера 
        WHERE Фамилия = %s AND Имя = %s AND Отчество = %s
        """
        result = self.db_manager.execute_query(check_name_query, (surname, name, patronymic), fetch=True)
        
        if result and result[0]['count'] > 0:
            QMessageBox.warning(self, "Ошибка", "Тренер с таким ФИО уже существует!")
            return False

        # Проверка на дубликат номера телефона
        if number:
            check_phone_query = "SELECT COUNT(*) as count FROM Тренера WHERE Телефон = %s"
            result = self.db_manager.execute_query(check_phone_query, (number,), fetch=True)
            
            if result and result[0]['count'] > 0:
                QMessageBox.warning(self, "Ошибка", "Тренер с таким номером телефона уже существует!")
                return False

        if not self.view_mode:
            try:  
                query = """
                INSERT INTO Тренера (Фамилия, Имя, Отчество, Доп_информация, Телефон)
                VALUES (%s, %s, %s, %s, %s)
                """
                params = (surname, name, patronymic, info, number)
                self.db_manager.execute_query(query, params)

                # Очистка формы после успешного добавления
                self.surname_coach.clear()
                self.name_coach.clear()
                self.otchestvo_coach.clear()
                self.dopinfo_coach.clear()
                self.number_coach.clear()

                if self.parent():
                    if hasattr(self.parent(), 'load_trainers'):
                        self.parent().load_trainers()
                    if hasattr(self.parent(), 'load_coaches'):
                        self.parent().load_coaches()
                
                self.accept()
                return True

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить тренера: {e}")
                return False
            
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

        self.number_coach.setPlaceholderText("Номер телефона")
        self.number_coach.setInputMask("")

        self.number_coach.textEdited.connect(self.apply_input_mask)
        self.number_coach.cursorPositionChanged.connect(self.adjust_cursor_position)

    def apply_input_mask(self):
        # Если текст пустой, сбрасываем маску
        if not self.number_coach.text():
            self.number_coach.setInputMask("")
            self.number_coach.setPlaceholderText("Номер телефона")
        elif not self.number_coach.inputMask():
            self.number_coach.setInputMask('+7(999) 999-99-99')
            self.number_coach.setCursorPosition(4)

    def adjust_cursor_position(self):
        if self.number_coach.cursorPosition() < 3:
            self.number_coach.setCursorPosition(3)

    def set_coach_data(self, coach_id, surname, name, patronymic, info, number):
        self.current_coach_id = coach_id
        self.surname_coach.setText(surname)
        self.name_coach.setText(name)
        self.otchestvo_coach.setText(patronymic)
        self.dopinfo_coach.setPlainText(info)
        self.number_coach.setText(number)

    def save_coach_changes(self):
        new_surname = self.name_coach.text().strip()
        new_name = self.surname_coach.text().strip()
        new_patronymic = self.otchestvo_coach.text().strip()
        new_info = self.dopinfo_coach.toPlainText().strip()
        
        if self.number_coach.text().replace('(', '').replace(')', '').replace('-', '').replace(' ', '').strip() == '+7':
            new_number = ''  # Считаем поле пустым
        else:
            raw_number = ''.join(filter(str.isdigit, self.number_coach.text()))
            if raw_number:
                # Проверка на полноту номера
                if len(raw_number) != 11:
                    QMessageBox.warning(self, "Ошибка", "Номер телефона введен не полностью!")
                    return
                if raw_number.startswith('7'):
                    raw_number = raw_number[1:]
                new_number = f'+7{raw_number}'
            else:
                new_number = ''

        if not new_surname or not new_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и Имя обязательны для заполнения!")
            return

        try:
            # Проверка на дубликат ФИО
            check_name_query = """
            SELECT COUNT(*) as count FROM Тренера 
            WHERE Фамилия = %s AND Имя = %s AND Отчество = %s 
            AND id_Тренера != %s
            """
            result = self.db_manager.execute_query(check_name_query, 
                (new_surname, new_name, new_patronymic, self.current_coach_id), fetch=True)
            
            if result and result[0]['count'] > 0:
                QMessageBox.warning(self, "Ошибка", "Тренер с таким ФИО уже существует!")
                return

            # Проверка на дубликат номера телефона
            if new_number:
                check_phone_query = """
                SELECT COUNT(*) as count FROM Тренера 
                WHERE Телефон = %s AND id_Тренера != %s
                """
                result = self.db_manager.execute_query(check_phone_query, 
                    (new_number, self.current_coach_id), fetch=True)
                
                if result and result[0]['count'] > 0:
                    QMessageBox.warning(self, "Ошибка", "Тренер с таким номером телефона уже существует!")
                    return

            update_query = """
            UPDATE Тренера 
            SET Фамилия = %s, Имя = %s, Отчество = %s, Доп_информация = %s, Телефон = %s 
            WHERE id_Тренера = %s
            """
            
            self.db_manager.execute_query(update_query, 
                (new_surname, new_name, new_patronymic, new_info, new_number, self.current_coach_id))
            
            # Обновляем таблицы в родительском окне
            if self.parent():
                if hasattr(self.parent(), 'load_trainers'):
                    self.parent().load_trainers()
                if hasattr(self.parent(), 'load_coaches'):
                    self.parent().load_coaches()
            
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные тренера: {e}")

class MainWindow(QDialog, Ui_Mainwindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db_manager = DatabaseManager(
            host="127.0.0.1",
            user="root",
            password="qwerty123",
            db_name="hand_combat",
            charset="utf8mb4",
            encryption_key=ENCRYPTION_KEY
        )

        encrypted_login = self.db_manager.crypto.encrypt('admin'.encode())
        encrypted_password = self.db_manager.crypto.encrypt('123'.encode())

        # Обновляем значения в базе данных
        query = "UPDATE admin_user SET login = %s, password = %s WHERE id = 2"
        self.db_manager.execute_query(query, (encrypted_login, encrypted_password))
        self.load_trainers()
        self.load_groups()
        self.load_sportmen()
        self.load_trainings
        self.load_groups_for_calendar()
        self.setup_backup_button()
        
        self.setup_attendance_tab()
        self.rank_sort_order = Qt.AscendingOrder
        
        self.tableposeshaem.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableposeshaem.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setup_attendance_tab()
        self.setup_reporting_tab()

        # Подключаем сигнал выбора группы
        self.grupaBox_tab1.currentIndexChanged.connect(self.on_group_selected)

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

        self.calendarWidget.activated.connect(self.on_calendar_double_clicked)
        self.calendarWidget.selectionChanged.connect(self.on_calendar_date_changed)

        self.tableWidget_tab4.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        self.date_sort_order = Qt.AscendingOrder  # Добавляем переменную для отслеживания порядка сортировки

        self.addbutton_tab2.clicked.connect(self.open_create_tren_dialog)
        self.izmenbutton_tab2.clicked.connect(self.on_izmenbutton_clicked)
        self.delbutton_tab2.clicked.connect(self.del_tren_dialog)

        self.addbutton_tab3.clicked.connect(self.create_coach_dialog)
        self.izmenbutton_tab3.clicked.connect(self.edit_coach)
        self.delbutton_tab3.clicked.connect(self.del_coach_dialog)

        self.addbutton_tab4.clicked.connect(self.create_sportman_dialog)
        self.izmenbutton_tab4.clicked.connect(self.edit_sportsman)
        self.delbutton_tab4.clicked.connect(self.del_sportman_dialog)

        self.addbutton_tab5.clicked.connect(self.create_gruppa_dialog)
        self.izmenbutton_tab5.clicked.connect(self.edit_group)
        self.delbutton_tab5.clicked.connect(self.del_group_dialog)

        self.clearbutton_tab6.clicked.connect(self.del_otchet_dialog)
        # Поиск для тренеров
        self.search_coach = QtWidgets.QLineEdit(self.tab_6)  # Привязываем к вкладке тренеров
        self.search_coach.setGeometry(QtCore.QRect(900, 20, 200, 30))
        self.search_coach.setPlaceholderText("Поиск тренера...")
        self.search_coach.textChanged.connect(self.search_coaches)
        self.search_coach.setMaxLength(20)

        # Поиск для спортсменов
        self.search_sportsman = QtWidgets.QLineEdit(self.tab_5)  # Привязываем к вкладке спортсменов
        self.search_sportsman.setGeometry(QtCore.QRect(900, 20, 200, 30))
        self.search_sportsman.setPlaceholderText("Поиск спортсмена...")
        self.search_sportsman.textChanged.connect(self.search_sportsmen)
        self.search_sportsman.setMaxLength(20)

        # Поиск для групп
        self.search_group = QtWidgets.QLineEdit(self.tab)  # Привязываем к вкладке групп
        self.search_group.setGeometry(QtCore.QRect(900, 20, 200, 30))
        self.search_group.setPlaceholderText("Поиск группы...")
        self.search_group.textChanged.connect(self.search_groups)
        self.search_group.setMaxLength(20)

        search_style = """
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """
        self.search_coach.setStyleSheet(search_style)
        self.search_sportsman.setStyleSheet(search_style)
        self.search_group.setStyleSheet(search_style)

        self.grupaBox_tab2.setFocusPolicy(Qt.NoFocus)
        self.grupaBox_tab1.setFocusPolicy(Qt.NoFocus)
        self.grupaBox_tab6.setFocusPolicy(Qt.NoFocus)

        self.login_window = LoginSystem(self.db_manager)
        if self.login_window.exec_() != QDialog.Accepted:
            return  
        self.show()

    def search_coaches(self):
        search_text = self.search_coach.text().lower()
        for row in range(self.tableWidget_tab3.rowCount()):
            show_row = False
            for col in range(self.tableWidget_tab3.columnCount()):
                item = self.tableWidget_tab3.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.tableWidget_tab3.setRowHidden(row, not show_row)

    def search_sportsmen(self):
        search_text = self.search_sportsman.text().lower()
        for row in range(self.tableWidget_tab4.rowCount()):
            show_row = False
            for col in range(self.tableWidget_tab4.columnCount()):
                item = self.tableWidget_tab4.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.tableWidget_tab4.setRowHidden(row, not show_row)

    def search_groups(self):
        search_text = self.search_group.text().lower()
        for row in range(self.tableWidget_tab5.rowCount()):
            show_row = False
            for col in range(self.tableWidget_tab5.columnCount()):
                item = self.tableWidget_tab5.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.tableWidget_tab5.setRowHidden(row, not show_row)

    def check_training_exists(self, group_id, date):
        query = """
        SELECT COUNT(*) as count 
        FROM Расписание_тренировок 
        WHERE id_Группы = %s AND DATE(Дата_время) = %s
        """
        result = self.db_manager.execute_query(query, (group_id, date), fetch=True)
        return result[0]['count'] > 0

    def check_group_selected(self):
        selected_group = self.grupaBox_tab2.currentText()
        if selected_group == "Выбор группы":
            QMessageBox.warning(
                self,
                "Внимание",
                "Пожалуйста, выберите группу!"
            )
            return False
        return True

    def open_create_tren_dialog(self):
        if not self.check_group_selected():
            return
                
        selected_date = self.calendarWidget.selectedDate()
        selected_group = self.grupaBox_tab2.currentText()
        group_id = self.calendar_group_ids[selected_group]
        
        # Проверяем существование тренировки на выбранную дату
        if self.check_training_exists(group_id, selected_date.toPyDate()):
            QMessageBox.warning(
                self, 
                "Внимание", 
                "На этот день уже назначена тренировка для данной группы!"
            )
            return
        
        create_tren_dialog = CreateTren(self.db_manager, self)
        
        # Устанавливаем выбранную дату и время
        current_time = QtCore.QTime.currentTime()
        selected_datetime = QtCore.QDateTime(selected_date, current_time)
        create_tren_dialog.dateTimeEdit_soztren.setDateTime(selected_datetime)
        
        # Получаем тренера для выбранной группы
        query = """
        SELECT CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) as ФИО
        FROM Группы г
        JOIN Тренера т ON г.id_Тренера = т.id_Тренера
        WHERE г.Название = %s
        """
        result = self.db_manager.execute_query(query, (selected_group,), fetch=True)
        
        if result:
            trainer_name = result[0]['ФИО']
            # Очищаем и добавляем только нужного тренера
            create_tren_dialog.trenerBox_soztren.clear()
            create_tren_dialog.trenerBox_soztren.addItem(trainer_name)
            create_tren_dialog.trenerBox_soztren.setEnabled(False)
        
        # Устанавливаем группу
        create_tren_dialog.grupaBox_soztren.clear()
        create_tren_dialog.grupaBox_soztren.addItem(selected_group)
        create_tren_dialog.grupaBox_soztren.setEnabled(False)
        
        if create_tren_dialog.exec_() == QDialog.Accepted:
            format = QtGui.QTextCharFormat()
            self.calendarWidget.setDateTextFormat(QtCore.QDate(), format)
            self.load_calendar_trainings(group_id)

    def load_trainings(self):
        try:
            query = """
            SELECT тр.id_Тренировки, тр.Название, 
                CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) as Тренер,
                г.Название as Группа, тр.Дата_время
            FROM Тренировки тр
            JOIN Тренера т ON тр.id_Тренера = т.id_Тренера
            JOIN Группы г ON тр.id_Группы = г.id_Группы
            ORDER BY тр.Дата_время DESC
            """
            trainings = self.db_manager.execute_query(query, fetch=True)
            
            # Configure table
            self.tableWidget_tab2.clearContents()
            self.tableWidget_tab2.setRowCount(len(trainings))
            self.tableWidget_tab2.setColumnCount(5)
            self.tableWidget_tab2.setHorizontalHeaderLabels([
                'ID', 'Название', 'Тренер', 'Группа', 'Дата и время'
            ])
            
            # Set table properties
            self.tableWidget_tab2.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tableWidget_tab2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget_tab2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            
            # Fill table
            for row, training in enumerate(trainings):
                self.tableWidget_tab2.setItem(row, 0, QTableWidgetItem(str(training['id_Тренировки'])))
                self.tableWidget_tab2.setItem(row, 1, QTableWidgetItem(training['Название']))
                self.tableWidget_tab2.setItem(row, 2, QTableWidgetItem(training['Тренер']))
                self.tableWidget_tab2.setItem(row, 3, QTableWidgetItem(training['Группа']))
                self.tableWidget_tab2.setItem(row, 4, QTableWidgetItem(
                    training['Дата_время'].strftime('%d.%m.%Y %H:%M')
                ))
            
            # Hide ID column
            self.tableWidget_tab2.setColumnHidden(0, True)
            
            # Adjust column widths
            self.tableWidget_tab2.setColumnWidth(1, 200)
            self.tableWidget_tab2.setColumnWidth(2, 250)
            self.tableWidget_tab2.setColumnWidth(3, 200)
            self.tableWidget_tab2.setColumnWidth(4, 150)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить тренировки: {e}")

    def load_calendar_trainings(self, group_id=None):
        try:
            if group_id:
                query = """
                SELECT Дата_время 
                FROM Расписание_тренировок 
                WHERE id_Группы = %s
                """
                trainings = self.db_manager.execute_query(query, (group_id,), fetch=True)
            else:
                query = "SELECT Дата_время FROM Расписание_тренировок"
                trainings = self.db_manager.execute_query(query, fetch=True)

            # Подсвечиваем даты тренировок на календаре
            for training in trainings:
                date = training['Дата_время'].date()
                format = QtGui.QTextCharFormat()
                format.setBackground(QtGui.QColor(173, 216, 230))  # Светло-голубой цвет
                self.calendarWidget.setDateTextFormat(QtCore.QDate(date.year, date.month, date.day), format)
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить тренировки: {e}")

    def load_groups_for_calendar(self):
        query = "SELECT id_Группы, Название FROM Группы"
        groups = self.db_manager.execute_query(query, fetch=True)
        
        self.grupaBox_tab2.clear()
        self.grupaBox_tab2.addItem("Выбор группы")
        
        self.calendar_group_ids = {}
        for group in groups:
            self.grupaBox_tab2.addItem(group['Название'])
            self.calendar_group_ids[group['Название']] = group['id_Группы']
        
        self.grupaBox_tab2.currentTextChanged.connect(self.on_calendar_group_changed)
        if hasattr(self, 'refresh_groups_combobox'):
            self.refresh_groups_combobox()

    def on_calendar_group_changed(self, group_name):
        # Очищаем форматирование календаря
        format = QtGui.QTextCharFormat()
        self.calendarWidget.setDateTextFormat(QtCore.QDate(), format)
        
        # Проверяем выбранную дату
        selected_date = self.calendarWidget.selectedDate()
        current_date = QtCore.QDate.currentDate()
        
        # Если пустая строка или "Выбор группы" - выходим
        if not group_name or group_name == "Выбор группы":
            return
            
        # Получаем id группы
        if group_name in self.calendar_group_ids:
            group_id = self.calendar_group_ids[group_name]
            self.load_calendar_trainings(group_id)
        else:
            # Обновляем список групп если группа не найдена
            self.load_groups_for_calendar()

    def on_calendar_date_changed(self):
        selected_date = self.calendarWidget.selectedDate()
        current_date = QtCore.QDate.currentDate()
        
        # Деактивируем кнопки если дата прошла
        self.addbutton_tab2.setEnabled(selected_date >= current_date)
        self.izmenbutton_tab2.setEnabled(selected_date >= current_date)
        self.delbutton_tab2.setEnabled(selected_date >= current_date)

    def on_calendar_double_clicked(self, date):    
        selected_group = self.grupaBox_tab2.currentText()
        
        if selected_group == "Выбор группы":
            return
        
        query = """
        SELECT рт.id_Тренировки, рт.Название, 
            CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) as Тренер,
            г.Название as Группа, рт.Дата_время
        FROM Расписание_тренировок рт
        JOIN Тренера т ON рт.id_Тренера = т.id_Тренера
        JOIN Группы г ON рт.id_Группы = г.id_Группы
        WHERE DATE(рт.Дата_время) = %s AND г.id_Группы = %s
        """
        
        group_id = self.calendar_group_ids[selected_group]
        trainings = self.db_manager.execute_query(query, (date.toPyDate(), group_id), fetch=True)
        
        if trainings:
            edit_tren = EditTren(self.db_manager, self, edit_mode=False)  # Изменено на False для режима просмотра
            training_data = {
                'id_Тренировки': trainings[0]['id_Тренировки'],
                'Название': trainings[0]['Название'],
                'Тренер': trainings[0]['Тренер'],
                'Группа': trainings[0]['Группа'],
                'Дата_время': trainings[0]['Дата_время']
            }
            edit_tren.set_training_data(training_data)
            
            # Блокируем все поля для режима просмотра
            edit_tren.trenerBox_soztren.setEnabled(False)
            edit_tren.grupaBox_soztren.setEnabled(False)
            edit_tren.name_tren.setEnabled(False)
            edit_tren.dateTimeEdit_soztren.setEnabled(False)
            edit_tren.addbutton_soztren.setEnabled(False)  # Скрываем кнопку сохранения
            
            edit_tren.exec_()

    def refresh_groups_tab2(self):
        self.grupaBox_tab2.clear()
        query = """
        SELECT DISTINCT г.Название
        FROM Группы г
        JOIN Тренера т ON г.id_Тренера = т.id_Тренера
        """
        groups = self.db_manager.execute_query(query, fetch=True)
        self.grupaBox_tab2.addItem("Выбор группы")
        for group in groups:
            self.grupaBox_tab2.addItem(group['Название'])

    def on_izmenbutton_clicked(self):
        selected_date = self.calendarWidget.selectedDate()
        selected_group = self.grupaBox_tab2.currentText()
        
        if selected_group == "Выбор группы":
            QMessageBox.warning(self, "Внимание", "Выберите группу!")
            return
                
        query = """
        SELECT рт.id_Тренировки, рт.Название, 
            т.id_Тренера,
            CONCAT(т.Фамилия, ' ', т.Имя, ' ', т.Отчество) as Тренер,
            г.Название as Группа, рт.Дата_время
        FROM Расписание_тренировок рт
        JOIN Тренера т ON рт.id_Тренера = т.id_Тренера
        JOIN Группы г ON рт.id_Группы = г.id_Группы
        WHERE DATE(рт.Дата_время) = %s AND г.id_Группы = %s
        """
        
        group_id = self.calendar_group_ids[selected_group]
        trainings = self.db_manager.execute_query(query, (selected_date.toPyDate(), group_id), fetch=True)
        
        if trainings:
            edit_tren = EditTren(self.db_manager, self, edit_mode=True)
            
            # Добавляем id тренера в словарь
            trainer_name = trainings[0]['Тренер']
            edit_tren.trainer_ids = {trainer_name: trainings[0]['id_Тренера']}
            
            # Устанавливаем данные
            edit_tren.trenerBox_soztren.clear()
            edit_tren.trenerBox_soztren.addItem(trainer_name)
            edit_tren.trenerBox_soztren.setEnabled(False)
            
            edit_tren.grupaBox_soztren.clear()
            edit_tren.grupaBox_soztren.addItem(trainings[0]['Группа'])
            edit_tren.grupaBox_soztren.setEnabled(False)
            
            training_data = {
                'id_Тренировки': trainings[0]['id_Тренировки'],
                'Название': trainings[0]['Название'],
                'Тренер': trainer_name,
                'Группа': trainings[0]['Группа'],
                'Дата_время': trainings[0]['Дата_время']
            }
            edit_tren.set_training_data(training_data)
            
            if edit_tren.exec_():
                self.load_calendar_trainings(group_id)

    def del_tren_dialog(self):
        if not self.check_group_selected():
            return
            
        del_tren = QDialog(self)
        uic.loadUi('forms/deleteconfirm.ui', del_tren)
        yes_button = del_tren.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_tren.findChild(QtWidgets.QPushButton, "pushButton")
        
        if yes_button:
            yes_button.clicked.connect(lambda: (self.on_deletebutton_clicked(), del_tren.close()))
        if no_button:
            no_button.clicked.connect(del_tren.close)
        
        del_tren.exec_()

    def on_deletebutton_clicked(self):
        if not self.check_group_selected():
            return
                
        selected_date = self.calendarWidget.selectedDate()
        selected_group = self.grupaBox_tab2.currentText()
        group_id = self.calendar_group_ids[selected_group]
        
        # Получаем id тренировки
        query = """
        SELECT id_Тренировки
        FROM Расписание_тренировок
        WHERE DATE(Дата_время) = %s AND id_Группы = %s
        """
        result = self.db_manager.execute_query(query, (selected_date.toPyDate(), group_id), fetch=True)
        
        if result:
            training_id = result[0]['id_Тренировки']
            
            # Сначала удаляем записи посещаемости
            delete_attendance_query = """
            DELETE FROM Посещаемость
            WHERE DATE(Дата_время) = %s AND id_Группы = %s
            """
            self.db_manager.execute_query(delete_attendance_query, (selected_date.toPyDate(), group_id))
            
            # Затем удаляем тренировку
            delete_query = """
            DELETE FROM Расписание_тренировок
            WHERE id_Тренировки = %s
            """
            self.db_manager.execute_query(delete_query, (training_id,))
            
            # Очищаем подсветку для удаленной даты
            format = QtGui.QTextCharFormat()
            self.calendarWidget.setDateTextFormat(selected_date, format)
            
            self.load_calendar_trainings(group_id)
            
            # Обновляем таблицу посещаемости
            self.refresh_attendance_list()
        else:
            QMessageBox.warning(self, "Внимание", "На выбранную дату нет тренировок!")

    def create_coach_dialog(self):
        create_coach_dialog = CreateCoachDialog(self.db_manager, self)
        if create_coach_dialog.exec_():
            self.load_trainers()

    def format_phone_number(self, phone):
        if phone and len(phone) >= 11:
            # Убираем все нецифровые символы
            digits = ''.join(filter(str.isdigit, phone))
            # Форматируем номер
            return f'+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}'
        return phone

    def load_trainers(self):
        try:
            connection = connect_to_db()
            if not connection:
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных!")
                return

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = "SELECT id_Тренера, Фамилия, Имя, Отчество, Доп_информация, Телефон FROM Тренера"
                cursor.execute(query)
                trainers = cursor.fetchall()

            # Очищаем таблицу
            self.tableWidget_tab3.clearContents()
            self.tableWidget_tab3.setRowCount(len(trainers))
            self.tableWidget_tab3.setColumnCount(6)
            self.tableWidget_tab3.setHorizontalHeaderLabels(['Фамилия', 'Имя', 'Отчество', 'Дополнительная информация', 'Телефон'])

            self.tableWidget_tab3.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tableWidget_tab3.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.tableWidget_tab3.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.tableWidget_tab3.setColumnWidth(0, 250)
            self.tableWidget_tab3.setColumnWidth(1, 250)
            self.tableWidget_tab3.setColumnWidth(2, 250)
            self.tableWidget_tab3.setColumnWidth(3, 300)
            self.tableWidget_tab3.setColumnWidth(4, 170)

            self.tableWidget_tab3.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows) 
            self.tableWidget_tab3.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

            self.tableWidget_tab3.setColumnHidden(3, True)
            self.tableWidget_tab3.setColumnHidden(5, True)


            for row_index, trainer in enumerate(trainers):
                id_item = QTableWidgetItem(str(trainer['id_Тренера']))
                self.tableWidget_tab3.setItem(row_index, 5, id_item)
                
                # Меняем порядок заполнения данных
                self.tableWidget_tab3.setItem(row_index, 0, QTableWidgetItem(trainer['Фамилия']))  # Фамилия в колонку Имя
                self.tableWidget_tab3.setItem(row_index, 1, QTableWidgetItem(trainer['Имя']))      # Имя в колонку Фамилия
                self.tableWidget_tab3.setItem(row_index, 2, QTableWidgetItem(trainer['Отчество']))
                self.tableWidget_tab3.setItem(row_index, 3, QTableWidgetItem(trainer['Доп_информация']))
                formatted_phone = self.format_phone_number(trainer['Телефон'])
                self.tableWidget_tab3.setItem(row_index, 4, QTableWidgetItem(formatted_phone))

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
        number = self.tableWidget_tab3.item(row, 4).text()

        # Открываем диалоговое окно для просмотра тренера
        create_coach_dialog = CreateCoachDialog(self.db_manager, self, view_mode=True)
        create_coach_dialog.surname_coach.setText(surname)
        create_coach_dialog.name_coach.setText(name)
        create_coach_dialog.otchestvo_coach.setText(patronymic)
        create_coach_dialog.dopinfo_coach.setPlainText(info)
        
        # Устанавливаем маску только если есть номер
        if number and number != '+7() --':
            create_coach_dialog.number_coach.setInputMask('+7 (999) 999-99-99')
            create_coach_dialog.number_coach.setText(number)
        else:
            create_coach_dialog.number_coach.setInputMask('')
            create_coach_dialog.number_coach.setText('')
        
        create_coach_dialog.surname_coach.setReadOnly(True)
        create_coach_dialog.name_coach.setReadOnly(True)
        create_coach_dialog.otchestvo_coach.setReadOnly(True)
        create_coach_dialog.dopinfo_coach.setReadOnly(True)
        create_coach_dialog.number_coach.setReadOnly(True)
        create_coach_dialog.addbutton_coach.setEnabled(False)
        create_coach_dialog.exec_()

    def edit_coach(self):
        self.open_edit_coach_dialog()

    def open_edit_coach_dialog(self):
        selected_row = self.tableWidget_tab3.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите тренера для редактирования!")
            return

        # Исправляем порядок получения данных из таблицы
        name = self.tableWidget_tab3.item(selected_row, 0).text()  # Фамилия в колонке 0
        surname = self.tableWidget_tab3.item(selected_row, 1).text()     # Имя в колонке 1
        patronymic = self.tableWidget_tab3.item(selected_row, 2).text() # Отчество в колонке 2
        info = self.tableWidget_tab3.item(selected_row, 3).text()
        number = self.tableWidget_tab3.item(selected_row, 4).text()

        edit_dialog = EditCoachDialog(self.db_manager, self)
        edit_dialog.set_coach_data(self.get_coach_id(name, surname, patronymic), 
                                surname, name, patronymic, info, number)
        
        if edit_dialog.exec_() == QDialog.Accepted:
            self.load_trainers()
            self.load_groups()
            self.load_sportmen()

    def get_coach_id(self, surname, name, patronymic):
        coach_id_query = """
        SELECT id_Тренера 
        FROM Тренера 
        WHERE Фамилия = %s AND Имя = %s AND Отчество = %s
        """
        result = self.db_manager.execute_query(coach_id_query, (surname, name, patronymic), fetch=True)
        if not result:
            raise ValueError(f"Тренер {surname} {name} {patronymic} не найден в базе данных")
        return result[0]['id_Тренера']
    
    def del_coach(self):
        selected_row = self.tableWidget_tab3.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите тренера для удаления!")
            return

        # Получаем ID тренера
        coach_id = int(self.tableWidget_tab3.item(selected_row, 5).text())
        
        try:
            # Проверяем, есть ли группы у тренера
            check_query = """
            SELECT Название 
            FROM Группы 
            WHERE id_Тренера = %s
            """
            result = self.db_manager.execute_query(check_query, (coach_id,), fetch=True)
            
            if result:
                # Формируем список групп для сообщения
                groups = [group['Название'] for group in result]
                groups_str = "\n- ".join(groups)
                
                QMessageBox.warning(
                    self, 
                    "Невозможно удалить тренера",
                    f"Этот тренер не может быть удален, так как он тренирует следующие группы:\n- {groups_str}\n\n"
                    "Пожалуйста, назначьте другого тренера этим группам перед удалением."
                )
                return

            # Если групп нет, удаляем тренера
            delete_query = "DELETE FROM Тренера WHERE id_Тренера = %s"
            self.db_manager.execute_query(delete_query, (coach_id,))
            
            # Обновляем таблицу
            self.load_trainers()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить операцию: {e}")

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
        selected_items = self.tableWidget_tab4.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Предупреждение", "Выберите спортсмена для редактирования")
            return

        row = selected_items[0].row()
        
        # Получаем данные из таблицы
        surname = self.tableWidget_tab4.item(row, 0).text()
        name = self.tableWidget_tab4.item(row, 1).text()
        patronymic = self.tableWidget_tab4.item(row, 2).text()
        group = self.tableWidget_tab4.item(row, 3).text()
        birth_date = self.tableWidget_tab4.item(row, 4).text()
        rank = self.tableWidget_tab4.item(row, 5).text()

        # Получаем ID спортсмена из базы данных
        query = """
        SELECT id_Спортсмена 
        FROM Спортсмены 
        WHERE Фамилия = %s AND Имя = %s AND Отчество = %s
        """
        result = self.db_manager.execute_query(query, (surname, name, patronymic), fetch=True)
        
        if result:
            sportsman_id = result[0]['id_Спортсмена']
            edit_dialog = EditSportMan(self.db_manager, self)
            edit_dialog.set_sportsman_data(sportsman_id, surname, name, patronymic, group, birth_date, rank)
            
            if edit_dialog.exec_() == QDialog.Accepted:
                self.load_sportmen()
        else:
            QMessageBox.warning(self, "Ошибка", "Спортсмен не найден в базе данных!")

    def load_sportmen(self):
        try:
            connection = connect_to_db()
            if not connection:
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных!")
                return

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT с.Фамилия, с.Имя, с.Отчество, 
                    COALESCE(г.Название, 'Без группы') as Группа, 
                    с.Дата_рождения, с.Спортивный_разряд 
                FROM Спортсмены с
                LEFT JOIN Группы г ON с.id_Группы = г.id_Группы
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
                self.tableWidget_tab4.setItem(row_index, 0, QTableWidgetItem(sportman['Фамилия']))
                self.tableWidget_tab4.setItem(row_index, 1, QTableWidgetItem(sportman['Имя']))
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

        # Получаем ID спортсмена
        get_id_query = """
        SELECT id_Спортсмена 
        FROM Спортсмены 
        WHERE Фамилия = %s AND Имя = %s AND Отчество = %s
        """
        
        surname = self.tableWidget_tab4.item(selected_row, 0).text()
        name = self.tableWidget_tab4.item(selected_row, 1).text()
        patronymic = self.tableWidget_tab4.item(selected_row, 2).text()

        try:
            # Получаем ID спортсмена
            result = self.db_manager.execute_query(get_id_query, (surname, name, patronymic), fetch=True)
            if result:
                athlete_id = result[0]['id_Спортсмена']
                
                # Удаляем записи посещаемости
                self.db_manager.execute_query(
                    "DELETE FROM Посещаемость WHERE id_Спортсмена = %s", 
                    (athlete_id,)
                )
                
                # Удаляем спортсмена
                self.db_manager.execute_query(
                    "DELETE FROM Спортсмены WHERE id_Спортсмена = %s", 
                    (athlete_id,)
                )
                
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

    def del_group_dialog(self):
        del_group = QDialog(self)
        uic.loadUi('forms/del_gruppa.ui', del_group)
        yes_button = del_group.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_group.findChild(QtWidgets.QPushButton, "pushButton")

        if yes_button:
            yes_button.clicked.connect(lambda: (self.delete_group(), del_group.close()))
        if no_button:
            no_button.clicked.connect(del_group.close)

        del_group.exec_()

    def create_gruppa_dialog(self):
        create_gruppa = CreateGruppaDialog(db_manager=self.db_manager, parent=self)
        if create_gruppa.exec_() == QDialog.Accepted:
            self.refresh_groups_tab2()  # Обновляем список групп
            self.load_groups()  # Обновляем таблицу групп
            self.load_groups_for_calendar() 

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
            self.tableWidget_tab5.setColumnWidth(1, 300)
            self.tableWidget_tab5.setColumnWidth(2, 550)

            self.tableWidget_tab5.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows) 
            self.tableWidget_tab5.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            header = self.tableWidget_tab5.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Fixed)
            
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
        group_id = self.tableWidget_tab5.item(row, 0).text()
        group_name = self.tableWidget_tab5.item(row, 1).text()
        trainer_name = self.tableWidget_tab5.item(row, 2).text()
        
        # Создаём диалог в режиме просмотра
        view_dialog = EditGruppaDialog(self.db_manager, self, view_mode=True)
        
        # Устанавливаем данные группы
        view_dialog.set_group_data(group_id, group_name, trainer_name)
        
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
        
        try:
            # Удаляем записи посещаемости
            delete_attendance_query = "DELETE FROM Посещаемость WHERE id_Группы = %s"
            self.db_manager.execute_query(delete_attendance_query, (group_id,))
            
            # Удаляем записи из расписания тренировок
            delete_schedule_query = "DELETE FROM Расписание_тренировок WHERE id_Группы = %s"
            self.db_manager.execute_query(delete_schedule_query, (group_id,))
            
            # Обновляем записи спортсменов
            update_athletes_query = "UPDATE Спортсмены SET id_Группы = NULL WHERE id_Группы = %s"
            self.db_manager.execute_query(update_athletes_query, (group_id,))
            
            # Удаляем группу
            delete_group_query = "DELETE FROM Группы WHERE id_Группы = %s"
            self.db_manager.execute_query(delete_group_query, (group_id,))
            
            # Обновляем все списки
            self.load_groups()
            self.load_sportmen()
            self.refresh_groups_tab2()
            self.load_groups_for_calendar()
            self.refresh_groups_combobox()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить группу: {e}")

    def get_training_dates(self, group_id, current_date):
        # Получаем даты тренировок для выбранной группы за текущий месяц
        query = """
        SELECT DISTINCT DATE(Дата_время) as Дата
        FROM Расписание_тренировок
        WHERE id_Группы = %s 
        AND MONTH(Дата_время) = %s 
        AND YEAR(Дата_время) = %s 
        ORDER BY Дата
        """
        
        current_month = current_date.month()
        current_year = current_date.year()
        
        training_dates = self.db_manager.execute_query(query, 
            (group_id, current_month, current_year), fetch=True)
        
        dates_formatted = []
        for date in training_dates:
            qdate = QDate.fromString(str(date['Дата']), 'yyyy-MM-dd')
            dates_formatted.append(qdate.toString('dd.MM'))
        
        return dates_formatted

    def get_group_athletes(self, group_id):
        query = """
        SELECT с.id_Спортсмена, с.Фамилия, с.Имя, с.Отчество
        FROM Спортсмены с
        WHERE с.id_Группы = %s
        ORDER BY с.Фамилия, с.Имя
        """
        return self.db_manager.execute_query(query, (group_id,), fetch=True)

    def get_athlete_id(self, row):
        # Получаем id спортсмена из таблицы по номеру строки
        athlete_data = self.get_group_athletes(self.grupaBox_tab1.currentData())
        return athlete_data[row]['id_Спортсмена']

    def get_date_from_column(self, col):
        # Получаем дату из заголовка колонки
        date_text = self.tableposeshaem.horizontalHeaderItem(col).text()
        # Преобразуем формат дд.ММ в корректный YYYY-MM-DD
        day, month = date_text.split('.')
        current_year = QDate.currentDate().year()
        formatted_date = f"{current_year}-{month}-{day} 00:00:00"
        return formatted_date

    def setup_attendance_columns(self):
        current_date = QDate.currentDate()
        group_id = self.grupaBox_tab1.currentData()
        
        if group_id is None:
            return
            
        training_dates = self.get_training_dates(group_id, current_date)
        
        # Настраиваем колонки таблицы
        self.tableposeshaem.setColumnCount(len(training_dates) + 1)  # +1 для колонки с ФИО
        
        # Устанавливаем заголовки
        headers = ['ФИО']  # Первая колонка для ФИО
        headers.extend(training_dates)  # Добавляем даты тренировок
        
        self.tableposeshaem.setHorizontalHeaderLabels(headers)
        
        # Настраиваем ширину колонок
        self.tableposeshaem.setColumnWidth(0, 300)  # ФИО
        for i in range(1, len(headers)):
            self.tableposeshaem.setColumnWidth(i, 80)  # Колонки с датами

    def load_groups_to_combobox(self):
        query = "SELECT id_Группы, Название FROM Группы"
        groups = self.db_manager.execute_query(query, fetch=True)
        
        self.grupaBox_tab1.clear()
        for group in groups:
            self.grupaBox_tab1.addItem(group['Название'], group['id_Группы'])

    def on_group_selected(self):
        if self.grupaBox_tab1.currentIndex() == -1:
            return
            
        group_id = self.grupaBox_tab1.currentData()
        self.load_attendance_table(group_id)

    def load_attendance_table(self, group_id):
        current_date = QDate.currentDate()
        training_dates = self.get_training_dates(group_id, current_date)
        athletes = self.get_group_athletes(group_id)
        
        # Setup table structure
        self.tableposeshaem.clear()
        self.tableposeshaem.setRowCount(len(athletes))
        self.tableposeshaem.setColumnCount(len(training_dates) + 1)
        headers = ['ФИО'] + training_dates
        self.tableposeshaem.setHorizontalHeaderLabels(headers)
        
        # Fill table
        for row, athlete in enumerate(athletes):
            # Set athlete name
            self.tableposeshaem.setItem(row, 0, QTableWidgetItem(
                f"{athlete['Фамилия']} {athlete['Имя']} {athlete['Отчество']}"
            ))
            
            # Add checkboxes
            for col, date in enumerate(training_dates, start=1):
                checkbox = QCheckBox()
                training_date = QDate.fromString(date, 'dd.MM')
                training_date = QDate(current_date.year(), training_date.month(), training_date.day())
                
                if training_date > current_date:
                    checkbox.setEnabled(False)
                    
                self.tableposeshaem.setCellWidget(row, col, checkbox)
                checkbox.stateChanged.connect(
                    lambda state, r=row, c=col: self.on_attendance_changed(r, c, state)
                )
        
        # Load existing marks
        self.load_attendance_marks(group_id, training_dates, athletes)
        
        # Set column widths
        self.tableposeshaem.setColumnWidth(0, 300)
        for col in range(1, len(training_dates) + 1):
            self.tableposeshaem.setColumnWidth(col, 80)
        header = self.tableposeshaem.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)

    def after_athlete_added(self):
        group_id = self.grupaBox_tab1.currentData()
        if group_id:
            self.load_attendance_table(group_id)

    def refresh_attendance_list(self):
        group_id = self.grupaBox_tab1.currentData()
        if group_id:
            self.load_attendance_table(group_id)

    def setup_attendance_tab(self):
        # Инициализация вкладки посещаемости
        self.load_groups_to_combobox()
        self.rank_sort_order = Qt.AscendingOrder
        
        # Подключаем сигнал выбора группы
        self.grupaBox_tab1.currentIndexChanged.connect(self.on_group_selected)

    def on_attendance_changed(self, row, col, state):
        group_id = self.grupaBox_tab1.currentData()
        athlete_id = self.get_athlete_id(row)
        date = self.get_date_from_column(col)
        
        attendance_value = 1 if state == Qt.Checked else 0
        
        # Сохраняем отметку в БД
        self.save_attendance_mark(group_id, athlete_id, date, attendance_value)

    def save_attendance_mark(self, group_id, athlete_id, date, value):
        query = """
        INSERT INTO Посещаемость (id_Спортсмена, id_Группы, Дата_время, Отметка)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE Отметка = %s
        """
        self.db_manager.execute_query(query, 
            (athlete_id, group_id, date, value, value)
        )

    def load_attendance_marks(self, group_id, training_dates, athletes):
        query = """
        SELECT id_Спортсмена, DATE(Дата_время) as Дата, Отметка 
        FROM Посещаемость 
        WHERE id_Группы = %s
        """
        attendance_records = self.db_manager.execute_query(query, (group_id,), fetch=True)
        
        # Create dictionary for quick access to marks
        attendance_dict = {}
        for record in attendance_records:
            date_str = record['Дата'].strftime('%d.%m')
            key = (record['id_Спортсмена'], date_str)
            attendance_dict[key] = record['Отметка']
        
        current_date = QDate.currentDate()
        
        # Set checkbox states
        for row, athlete in enumerate(athletes):
            for col, date in enumerate(training_dates, start=1):
                checkbox = self.tableposeshaem.cellWidget(row, col)
                if checkbox:
                    training_date = QDate.fromString(date, 'dd.MM')
                    training_date = training_date.addYears(current_date.year() - training_date.year())
                    
                    # Disable checkbox for future dates
                    if training_date > current_date:
                        checkbox.setEnabled(False)
                    else:
                        checkbox.setEnabled(True)
                        key = (athlete['id_Спортсмена'], date)
                        is_checked = attendance_dict.get(key, 0) == 1
                        checkbox.setChecked(is_checked)

    def refresh_groups_combobox(self):
        current_group_id = self.grupaBox_tab1.currentData()
        current_group_id2 = self.grupaBox_tab2.currentData()
        current_group_tab6 = self.grupaBox_tab6.currentText() if self.grupaBox_tab6.currentText() else "Все группы"
        
        self.load_groups_to_combobox()
        self.load_groups_for_reporting()
        
        # Восстанавливаем выбранную группу для первого комбобокса
        index = self.grupaBox_tab1.findData(current_group_id)
        if index >= 0:
            self.grupaBox_tab1.setCurrentIndex(index)
        
        # Восстанавливаем выбранную группу для второго комбобокса
        index2 = self.grupaBox_tab2.findData(current_group_id2)
        if index2 >= 0:
            self.grupaBox_tab2.setCurrentIndex(index2)

        index6 = self.grupaBox_tab6.findText(current_group_tab6)
        if index6 >= 0:
            self.grupaBox_tab6.setCurrentIndex(index6)

    def setup_reporting_tab(self):
        # Настраиваем ListView для общей статистики
        self.model_stats = QStandardItemModel()
        self.listView_tab6.setModel(self.model_stats)
        self.listView_tab6.setFocusPolicy(Qt.NoFocus)
        self.listView_tab6.setSelectionMode(QAbstractItemView.NoSelection)
        self.listView_tab6.setEditTriggers(QTableWidget.NoEditTriggers)
        self.load_groups_for_reporting()
        # Настраиваем таблицу посещаемости
        self.tableWidget_tab6.setColumnCount(2)
        self.tableWidget_tab6.setHorizontalHeaderLabels(['ФИО', 'Посещаемость, %'])
        self.tableWidget_tab6.setColumnWidth(0, 500)
        self.tableWidget_tab6.setColumnWidth(1, 130)
        self.tableWidget_tab6.setFocusPolicy(Qt.NoFocus)
        self.tableWidget_tab6.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableWidget_tab6.setEditTriggers(QTableWidget.NoEditTriggers)

        header = self.tableWidget_tab6.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        
        # Подключаем сигналы
        self.dateEdit_tab6.dateChanged.connect(self.update_reporting)
        self.grupaBox_tab6.currentIndexChanged.connect(self.update_reporting)

    def update_reporting(self):
        selected_date = self.dateEdit_tab6.date()
        selected_group = self.grupaBox_tab6.currentText()
        
        try:
            # Обновляем общую статистику в ListView
            self.update_general_stats()
            # Обновляем таблицу посещаемости
            self.update_attendance_table(selected_date, selected_group)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить отчетность: {e}")

        for row in range(self.tableWidget_tab6.rowCount()):
            attendance_item = self.tableWidget_tab6.item(row, 1)
            if attendance_item:
                attendance = float(attendance_item.text().replace('%', ''))
                color = self.get_color_for_attendance(attendance)
                for col in range(self.tableWidget_tab6.columnCount()):
                    self.tableWidget_tab6.item(row, col).setForeground(color)
        
        # For groups in listView_tab6
        for row in range(self.model_stats.rowCount()):
            item = self.model_stats.item(row)
            if item:
                text = item.text()
                if '%' in text:
                    attendance = float(text.split(':')[1].replace('%', '').strip())
                    color = self.get_color_for_attendance(attendance)
                    item.setForeground(color)

    def get_color_for_attendance(self, attendance):
        if attendance >= 65:
            return QtGui.QColor(0, 128, 0)  # Dark green
        elif 38 <= attendance < 65:
            return QtGui.QColor(184, 134, 11)  # Dark goldenrod
        else:
            return QtGui.QColor(178, 34, 34)  # Firebrick red

    def update_general_stats(self):
        try:
            self.model_stats.clear()
            
            # Получаем базовую статистику
            coaches_query = "SELECT COUNT(*) as count FROM Тренера"
            athletes_query = "SELECT COUNT(*) as count FROM Спортсмены"
            groups_query = "SELECT COUNT(*) as count FROM Группы"
            
            coaches_count = self.db_manager.execute_query(coaches_query, fetch=True)[0]['count']
            athletes_count = self.db_manager.execute_query(athletes_query, fetch=True)[0]['count']
            groups_count = self.db_manager.execute_query(groups_query, fetch=True)[0]['count']
            
            # Добавляем статистику в ListView
            self.model_stats.appendRow(QStandardItem(f"Количество действующих тренеров: {coaches_count}"))
            self.model_stats.appendRow(QStandardItem(f"Количество спортсменов: {athletes_count}"))
            self.model_stats.appendRow(QStandardItem(f"Количество групп: {groups_count}"))
            
            # Добавляем посещаемость по группам
            self.add_group_attendance_stats()
            
        except Exception as e:
            raise Exception(f"Ошибка при обновлении общей статистики: {e}")

    def load_groups_for_reporting(self):
        query = "SELECT id_Группы, Название FROM Группы"
        groups = self.db_manager.execute_query(query, fetch=True)
        
        self.grupaBox_tab6.clear()
        self.grupaBox_tab6.addItem("Все группы")  # Optional default item
        
        for group in groups:
            self.grupaBox_tab6.addItem(group['Название'])

    def add_group_attendance_stats(self):
        selected_date = self.dateEdit_tab6.date()
        start_of_month = selected_date.addDays(-selected_date.day() + 1)
        end_of_month = start_of_month.addMonths(1).addDays(-1)
        
        query = """
        SELECT 
            г.Название,
            COUNT(DISTINCT с.id_Спортсмена) as total_athletes,
            SUM(CASE WHEN п.Отметка = 1 AND DATE(п.Дата_время) <= CURRENT_DATE() THEN 1 ELSE 0 END) as total_visits,
            COUNT(DISTINCT CASE WHEN DATE(п.Дата_время) <= CURRENT_DATE() THEN DATE(п.Дата_время) END) as total_trainings
        FROM Группы г
        LEFT JOIN Спортсмены с ON г.id_Группы = с.id_Группы
        LEFT JOIN Посещаемость п ON с.id_Спортсмена = п.id_Спортсмена 
            AND DATE(п.Дата_время) BETWEEN %s AND %s
        GROUP BY г.id_Группы, г.Название
            """
        
        groups_data = self.db_manager.execute_query(
            query,
            (start_of_month.toString('yyyy-MM-dd'), end_of_month.toString('yyyy-MM-dd')),
            fetch=True
        )
        
        self.model_stats.appendRow(QStandardItem("\nПосещаемость по группам:"))
        
        for group in groups_data:
            print(f"Группа: {group['Название']}")
            print(f"Всего спортсменов: {group['total_athletes']}")
            print(f"Всего посещений: {group['total_visits']}")
            print(f"Всего тренировок: {group['total_trainings']}")
            
            if group['total_athletes'] > 0 and group['total_trainings'] > 0:
                attendance = (group['total_visits'] / 
                            (group['total_athletes'] * group['total_trainings'])) * 100
                self.model_stats.appendRow(
                    QStandardItem(f"{group['Название']}: {attendance:.1f}%")
                )

    def verify_attendance(self, athlete_id, group_id, date):
        query = """
        SELECT Отметка 
        FROM Посещаемость 
        WHERE id_Спортсмена = %s 
        AND id_Группы = %s 
        AND DATE(Дата_время) = %s
        """
        result = self.db_manager.execute_query(query, (athlete_id, group_id, date), fetch=True)
        return result[0]['Отметка'] if result else None

    def update_attendance_table(self, selected_date, selected_group):
        start_of_month = selected_date.addDays(-selected_date.day() + 1)
        end_of_month = start_of_month.addMonths(1).addDays(-1)

        print(f"Период: с {start_of_month.toString('yyyy-MM-dd')} по {end_of_month.toString('yyyy-MM-dd')}")
        print(f"Выбранная группа: {selected_group}")

        query = """
        WITH ПосещенияСпортсменов AS (
            SELECT 
                с.id_Спортсмена,
                CONCAT(с.Фамилия, ' ', с.Имя, ' ', с.Отчество) as ФИО,
                COUNT(DISTINCT rt.Дата_время) as total_trainings,
                COUNT(DISTINCT CASE WHEN п.Отметка = 1 THEN п.Дата_время END) as visits
            FROM Спортсмены с
            JOIN Группы г ON с.id_Группы = г.id_Группы
            LEFT JOIN Расписание_тренировок rt ON г.id_Группы = rt.id_Группы 
                AND DATE(rt.Дата_время) BETWEEN %s AND %s
                AND DATE(rt.Дата_время) <= CURRENT_DATE()
            LEFT JOIN Посещаемость п ON с.id_Спортсмена = п.id_Спортсмена 
                AND DATE(п.Дата_время) = DATE(rt.Дата_время)
            WHERE г.Название = %s
            GROUP BY с.id_Спортсмена, с.Фамилия, с.Имя, с.Отчество
        )
        SELECT 
            id_Спортсмена,
            ФИО,
            visits,
            total_trainings
        FROM ПосещенияСпортсменов
        ORDER BY ФИО
        """

        attendance_data = self.db_manager.execute_query(
            query, 
            (start_of_month.toString('yyyy-MM-dd'), 
            end_of_month.toString('yyyy-MM-dd'),
            selected_group),
            fetch=True
        )

        # Отладочный вывод
        for data in attendance_data:
            print(f"Спортсмен ID: {data['id_Спортсмена']}")
            print(f"ФИО: {data['ФИО']}")
            print(f"Посещений: {data['visits']}")
            print(f"Всего тренировок: {data['total_trainings']}")
            print("---")

        self.tableWidget_tab6.setRowCount(len(attendance_data))
        
        for row, data in enumerate(attendance_data):
            attendance_percent = 0
            if data['total_trainings'] > 0:
                attendance_percent = (data['visits'] / data['total_trainings']) * 100
                
            name_item = QTableWidgetItem(data['ФИО'])
            percent_item = QTableWidgetItem(f"{attendance_percent:.1f}%")
            
            self.tableWidget_tab6.setItem(row, 0, name_item)
            self.tableWidget_tab6.setItem(row, 1, percent_item)

    def check_athlete_attendance(self, athlete_id, start_date, end_date):
        query = """
        SELECT 
            DATE(Дата_время) as date,
            Отметка
        FROM Посещаемость
        WHERE id_Спортсмена = %s
        AND DATE(Дата_время) BETWEEN %s AND %s
        ORDER BY Дата_время
        """
        return self.db_manager.execute_query(query, (athlete_id, start_date, end_date), fetch=True)

    def del_otchet_dialog(self):
        del_otchet = QDialog(self)
        uic.loadUi('forms/del_otchet.ui', del_otchet)
        
        yes_button = del_otchet.findChild(QtWidgets.QPushButton, "pushButton_2")
        no_button = del_otchet.findChild(QtWidgets.QPushButton, "pushButton")
        
        if yes_button:
            yes_button.clicked.connect(self.clear_reporting_data)
        if no_button:
            no_button.clicked.connect(del_otchet.close)
        
        del_otchet.exec_()

    def clear_reporting_data(self):
        with QtCore.QSignalBlocker(self.dateEdit_tab6), QtCore.QSignalBlocker(self.grupaBox_tab6):

            self.model_stats.removeRows(0, self.model_stats.rowCount())
            self.tableWidget_tab6.clearContents()
            self.tableWidget_tab6.setRowCount(0)
            
            self.dateEdit_tab6.setDate(QDate.currentDate())
            self.grupaBox_tab6.setCurrentIndex(0)
        
        dialog = self.sender().parent() if self.sender() else None
        if dialog:
            dialog.close()

    def setup_backup_button(self):
        self.backup_button = QPushButton("Сохранить БД", self.tab_2)
        self.backup_button.setGeometry(QtCore.QRect(960, 430, 120, 25))
        self.backup_button.setStyleSheet("""
            QPushButton {
                background-color: #b0c4de;
                border-radius: 7%;
                border: 1px solid grey;
                font-family: Avenir Next;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #9db1cc;
            }
        """)
        self.backup_button.clicked.connect(self.create_database_backup)

    def create_database_backup(self):
        try:
            current_date = QDate.currentDate().toString('yyyy-MM-dd')
            
            file_name = f"hand_combat_backup_{current_date}.sql"
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить резервную копию",
                file_name,
                "MySQL Backup (*.sql)"
            )
            
            if save_path:
                command = f"mysqldump -u {self.db_manager.user} -p{self.db_manager.password} {self.db_manager.db_name} > {save_path}"
                
                result = os.system(command)
                
                if result == 0:
                    QMessageBox.information(
                        self,
                        "Успех",
                        f"Резервная копия успешно создана:\n{save_path}"
                    )
                else:
                    raise Exception("Ошибка при создании резервной копии")
                    
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось создать резервную копию: {str(e)}"
            )

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