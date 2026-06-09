from database import DatabaseManager
from mysql.connector import Error

class UsuarioDAO:
    def __init__(self):
        self.db = DatabaseManager()

    def insert(self, matricula, nome, telefone, data_nasc, cartao_acesso):
        self.db.connect()
        if self.db.conn:
            try:
                query = "INSERT INTO Usuario (matricula, nome, telefone, data_nasc, cartao_acesso) VALUES (%s, %s, %s, %s, %s)"
                self.db.cursor.execute(query, (matricula, nome, telefone, data_nasc, cartao_acesso))
                self.db.conn.commit()
                print(f"Usuário '{nome}' cadastrado com sucesso!")
            except Error as e:
                print(f"Erro ao inserir usuário: {e}")
            finally:
                self.db.close()

    def get_all(self):
        self.db.connect()
        if self.db.conn:
            try:
                self.db.cursor.execute("SELECT * FROM Usuario")
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []

    def update(self, matricula, novo_nome, novo_telefone):
        self.db.connect()
        if self.db.conn:
            try:
                query = "UPDATE Usuario SET nome = %s, telefone = %s WHERE matricula = %s"
                self.db.cursor.execute(query, (novo_nome, novo_telefone, matricula))
                self.db.conn.commit()
                print("Usuário atualizado com sucesso!")
            except Error as e:
                print(f"Erro ao atualizar usuário: {e}")
            finally:
                self.db.close()

    def delete(self, matricula):
        self.db.connect()
        if self.db.conn:
            try:
                query = "DELETE FROM Usuario WHERE matricula = %s"
                self.db.cursor.execute(query, (matricula,))
                self.db.conn.commit()
                print("Usuário removido com sucesso!")
            except Error as e:
                print(f"Erro ao deletar usuário: {e}")
            finally:
                self.db.close()

    def search_by_nome(self, nome):
        self.db.connect()
        if self.db.conn:
            try:
                query = "SELECT * FROM Usuario WHERE LOWER(nome) LIKE LOWER(%s)"
                self.db.cursor.execute(query, (f"%{nome}%",))
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []

    def get_usuario_com_cartao(self, matricula):
        self.db.connect()
        if self.db.conn:
            try:
                query = """
                    SELECT U.matricula, U.nome, C.codigo_de_barras, C.data_emissao, C.esta_ativo 
                    FROM Usuario U 
                    INNER JOIN Cartao_acesso C ON U.cartao_acesso = C.codigo_de_barras 
                    WHERE U.matricula = %s
                """
                self.db.cursor.execute(query, (matricula,))
                return self.db.cursor.fetchone()
            finally:
                self.db.close()
        return None