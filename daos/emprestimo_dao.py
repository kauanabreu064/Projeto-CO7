from database import DatabaseManager
from mysql.connector import Error

class EmprestimoDAO:
    def __init__(self):
        self.db = DatabaseManager()

    def insert(self, data_retirada, data_devolucao_prevista, usuario_id, valor_multa_diaria):
        self.db.connect()
        if self.db.conn:
            try:
                query = "INSERT INTO Emprestimo (data_retirada, data_devolucao_prevista, usuario, multa) VALUES (%s, %s, %s, %s)"
                self.db.cursor.execute(query, (data_retirada, data_devolucao_prevista, usuario_id, valor_multa_diaria))
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

    def get_divida_usuario(self, matricula):
        self.db.connect()
        if self.db.conn:
            try:
                query = """
                    SELECT id_emprestimo, data_devolucao_prevista, multa AS taxa_diaria,
                           (DATEDIFF(CURDATE(), data_devolucao_prevista) * multa) AS total_devido
                    FROM Emprestimo 
                    WHERE usuario = %s 
                      AND foi_devolvido = 0 
                      AND CURDATE() > data_devolucao_prevista
                """
                self.db.cursor.execute(query, (matricula,))
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []

    def get_todas_dividas(self):
        self.db.connect()
        if self.db.conn:
            try:
                query = """
                    SELECT E.id_emprestimo, E.data_devolucao_prevista, E.multa AS taxa_diaria, 
                           U.matricula, U.nome,
                           (DATEDIFF(CURDATE(), E.data_devolucao_prevista) * E.multa) AS total_devido
                    FROM Emprestimo E
                    INNER JOIN Usuario U ON E.usuario = U.matricula
                    WHERE E.foi_devolvido = 0 
                      AND CURDATE() > E.data_devolucao_prevista
                    ORDER BY total_devido DESC
                """
                self.db.cursor.execute(query)
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []