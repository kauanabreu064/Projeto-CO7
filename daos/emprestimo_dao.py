from database import DatabaseManager
from mysql.connector import Error

class EmprestimoDAO:
    def __init__(self):
        self.db = DatabaseManager()

    def insert(self, data_retirada, data_devolucao_prevista, usuario_id):
        self.db.connect()
        if self.db.conn:
            try:
                query = "INSERT INTO Emprestimo (data_retirada, data_devolucao_prevista, usuario) VALUES (%s, %s, %s)"
                self.db.cursor.execute(query, (data_retirada, data_devolucao_prevista, usuario_id))
                self.db.conn.commit()
                print("Empréstimo registrado com sucesso!")
            except Error as e:
                print(f"Erro ao criar empréstimo: {e}")
            finally:
                self.db.close()

    def get_all(self):
        self.db.connect()
        if self.db.conn:
            try:
                self.db.cursor.execute("SELECT * FROM Emprestimo")
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []

    def registrar_devolucao(self, id_emprestimo):
        self.db.connect()
        if self.db.conn:
            try:
                query = "UPDATE Emprestimo SET foi_devolvido = 1 WHERE id_emprestimo = %s"
                self.db.cursor.execute(query, (id_emprestimo,))
                self.db.conn.commit()
                print("Devolução registrada com sucesso!")
            except Error as e:
                print(f"Erro ao registrar devolução: {e}")
            finally:
                self.db.close()

    def delete(self, id_emprestimo):
        self.db.connect()
        if self.db.conn:
            try:
                query = "DELETE FROM Emprestimo WHERE id_emprestimo = %s"
                self.db.cursor.execute(query, (id_emprestimo,))
                self.db.conn.commit()
                print("Registro de empréstimo apagado.")
            except Error as e:
                print(f"Erro ao deletar empréstimo: {e}")
            finally:
                self.db.close()

    def search_by_usuario_id(self, matricula):
        self.db.connect()
        if self.db.conn:
            try:
                query = "SELECT * FROM Emprestimo WHERE usuario = %s"
                self.db.cursor.execute(query, (matricula,))
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []

    def get_emprestimos_com_usuarios(self):
        self.db.connect()
        if self.db.conn:
            try:
                query = """
                    SELECT E.id_emprestimo, E.data_retirada, E.foi_devolvido, U.nome, U.telefone 
                    FROM Emprestimo E
                    INNER JOIN Usuario U ON E.usuario = U.matricula
                """
                self.db.cursor.execute(query)
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []
    def update_multa(self, id_emprestimo, valor_multa):
        """UPDATE: Atualiza o valor da multa de um empréstimo atrasado"""
        self.db.connect()
        if self.db.conn:
            try:
                query = "UPDATE Emprestimo SET multa = %s WHERE id_emprestimo = %s"
                self.db.cursor.execute(query, (valor_multa, id_emprestimo))
                self.db.conn.commit()
                print(f"Multa de R$ {valor_multa:.2f} aplicada ao empréstimo {id_emprestimo}!")
            except Error as e:
                print(f"Erro ao atualizar multa: {e}")
            finally:
                self.db.close()

    def get_divida_usuario(self, matricula):
        """SELECT: Traz todos os empréstimos de um aluno que possuem multa e calcula o total"""
        self.db.connect()
        if self.db.conn:
            try:
                query = "SELECT id_emprestimo, data_retirada, multa, foi_devolvido FROM Emprestimo WHERE usuario = %s AND multa > 0"
                self.db.cursor.execute(query, (matricula,))
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []
