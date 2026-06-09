import mysql.connector
from mysql.connector import Error

def criar_conexao():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='library_db',
            user='root',
            password='root'
        )
        return conexao
    except Error as e:
        print(f"Erro crítico ao conectar ao Banco De Dados: {e}")
        return None