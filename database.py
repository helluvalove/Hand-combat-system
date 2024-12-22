import pymysql
import logging
from cryptography.fernet import Fernet

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, host, user, password, db_name, charset='utf8mb4', encryption_key=None):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.charset = charset
        self.crypto = Fernet(encryption_key) if encryption_key else None

    def connect_to_db(self):
        try:
            return pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise

    def execute_query(self, query, params=None, fetch=False):
        try:
            connection = self.connect_to_db()
            with connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    result = cursor.fetchall()
                else:
                    connection.commit()
                    result = True
                connection.close()
                return result
        except Exception as e:
            logger.error(f"Ошибка выполнения запроса: {e}")
            raise e

    def insert_trainer(self, surname, name, patronymic, info):
        query = """
            INSERT INTO Тренера (Фамилия, Имя, Отчество, Доп_информация)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (name, surname, patronymic, info))

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.crypto.encrypt(data)
    
    def decrypt(self, encrypted_data):
        return self.crypto.decrypt(encrypted_data).decode()