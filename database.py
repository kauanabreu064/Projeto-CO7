import mysql.connector
from config import MYSQL_CONFIG
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**MYSQL_CONFIG)
            self.cursor = self.conn.cursor(dictionary=True)
            return self.conn
        except Error as e:
            print(f"Erro de conexão com o MySQL: {e}")
            return None

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()