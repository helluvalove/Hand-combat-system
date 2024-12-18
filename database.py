import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, host, user, password, db_name, charset='utf8mb4'):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.charset = charset

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
        connection = self.connect_to_db()
        if not connection:
            return False
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                connection.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка выполнения запроса: {e}")
            return False
        finally:
            connection.close()

    def insert_trainer(self, surname, name, patronymic, info):
        query = """
            INSERT INTO Тренера (Фамилия, Имя, Отчество, Доп_информация)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (surname, name, patronymic, info))