
from database import DatabaseManager
from mysql.connector import Error

class AutorDAO:
    def __init__(self):
        self.db = DatabaseManager()

    def insert(self, nome, nacionalidade, data_nasc):
        self.db.connect()
        if self.db.conn:
            try:
                query = "INSERT INTO Autor (nome, nacionalidade, data_nasc) VALUES (%s, %s, %s)"
                self.db.cursor.execute(query, (nome, nacionalidade, data_nasc))
                self.db.conn.commit()
                print(f"Autor '{nome}' cadastrado com sucesso!")
            except Error as e:
                print(f"Erro ao inserir autor: {e}")
            finally:
                self.db.close()

    def get_all(self):
        """READ: Lista todos os autores"""
        self.db.connect()
        if self.db.conn:
            try:
                self.db.cursor.execute("SELECT * FROM Autor")
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []

    def update(self, id_autor, novo_nome, nova_nacionalidade):
        self.db.connect()
        if self.db.conn:
            try:
                query = "UPDATE Autor SET nome = %s, nacionalidade = %s WHERE id_autor = %s"
                self.db.cursor.execute(query, (novo_nome, nova_nacionalidade, id_autor))
                self.db.conn.commit()
                print("Dados do autor atualizados!")
            except Error as e:
                print(f"Erro ao atualizar autor: {e}")
            finally:
                self.db.close()

    def delete(self, id_autor):
        self.db.connect()
        if self.db.conn:
            try:
                query = "DELETE FROM Autor WHERE id_autor = %s"
                self.db.cursor.execute(query, (id_autor,))
                self.db.conn.commit()
                print("Autor removido do banco de dados.")
            except Error as e:
                print(f"Erro ao deletar autor: {e}")
            finally:
                self.db.close()

    def search_by_nome(self, nome):
        self.db.connect()
        if self.db.conn:
            try:
                query = "SELECT * FROM Autor WHERE LOWER(nome) LIKE LOWER(%s)"
                self.db.cursor.execute(query, (f"%{nome}%",))
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []