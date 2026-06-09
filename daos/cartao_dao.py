from database import DatabaseManager
from mysql.connector import Error

class CartaoDAO:
    def __init__(self):
        self.db = DatabaseManager()

    def insert(self, codigo_de_barras, data_emissao, esta_ativo=1):
        self.db.connect()
        if self.db.conn:
            try:
                query = "INSERT INTO Cartao_acesso (codigo_de_barras, data_emissao, esta_ativo) VALUES (%s, %s, %s)"
                self.db.cursor.execute(query, (codigo_de_barras, data_emissao, esta_ativo))
                self.db.conn.commit()
                print(f"Cartão {codigo_de_barras} gerado com sucesso!")
            except Error as e:
                print(f"Erro ao inserir cartão: {e}")
            finally:
                self.db.close()

    def get_all(self):
        self.db.connect()
        if self.db.conn:
            try:
                self.db.cursor.execute("SELECT * FROM Cartao_acesso")
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []

    def update_status(self, codigo_de_barras, novo_status):
        self.db.connect()
        if self.db.conn:
            try:
                query = "UPDATE Cartao_acesso SET esta_ativo = %s WHERE codigo_de_barras = %s"
                self.db.cursor.execute(query, (novo_status, codigo_de_barras))
                self.db.conn.commit()
                print("Status do cartão atualizado!")
            except Error as e:
                print(f"Erro ao atualizar cartão: {e}")
            finally:
                self.db.close()

    def delete(self, codigo_de_barras):
        self.db.connect()
        if self.db.conn:
            try:
                query = "DELETE FROM Cartao_acesso WHERE codigo_de_barras = %s"
                self.db.cursor.execute(query, (codigo_de_barras,))
                self.db.conn.commit()
                print("Cartão removido permanentemente.")
            except Error as e:
                print(f"Erro ao deletar cartão: {e}")
            finally:
                self.db.close()

    def search_by_codigo(self, codigo_de_barras):
        self.db.connect()
        if self.db.conn:
            try:
                query = "SELECT * FROM Cartao_acesso WHERE codigo_de_barras = %s"
                self.db.cursor.execute(query, (codigo_de_barras,))
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []
