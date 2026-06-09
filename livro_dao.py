from database import DatabaseManager
from mysql.connector import Error

class LivroDAO:
    def __init__(self):
        self.db = DatabaseManager()

    def insert(self, codigo_de_barras, nome, publicacao, valor_reposicao):
        self.db.connect()
        if self.db.conn:
            try:
                query = "INSERT INTO Livro (codigo_de_barras, nome, publicacao, valor_reposicao) VALUES (%s, %s, %s, %s)"
                self.db.cursor.execute(query, (codigo_de_barras, nome, publicacao, valor_reposicao))
                self.db.conn.commit()
                print(f"Livro '{nome}' adicionado ao catálogo!")
            except Error as e:
                print(f"Erro ao inserir livro: {e}")
            finally:
                self.db.close()

    def get_all(self):
        self.db.connect()
        if self.db.conn:
            try:
                self.db.cursor.execute("SELECT * FROM Livro")
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []

    def update_valor(self, codigo_de_barras, novo_valor):
        self.db.connect()
        if self.db.conn:
            try:
                query = "UPDATE Livro SET valor_reposicao = %s WHERE codigo_de_barras = %s"
                self.db.cursor.execute(query, (novo_valor, codigo_de_barras))
                self.db.conn.commit()
                print("Valor do livro atualizado!")
            except Error as e:
                print(f"Erro ao atualizar livro: {e}")
            finally:
                self.db.close()

    def delete(self, codigo_de_barras):
        self.db.connect()
        if self.db.conn:
            try:
                query = "DELETE FROM Livro WHERE codigo_de_barras = %s"
                self.db.cursor.execute(query, (codigo_de_barras,))
                self.db.conn.commit()
                print("Livro removido do acervo.")
            except Error as e:
                print(f"Erro ao deletar livro: {e}")
            finally:
                self.db.close()

    def search_by_titulo(self, titulo):
        self.db.connect()
        if self.db.conn:
            try:
                query = "SELECT * FROM Livro WHERE LOWER(nome) LIKE LOWER(%s)"
                self.db.cursor.execute(query, (f"%{titulo}%",))
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []

    def get_livros_com_autores(self):
        self.db.connect()
        if self.db.conn:
            try:
                query = """
                    SELECT L.nome AS livro, L.codigo_de_barras, A.nome AS autor, A.nacionalidade 
                    FROM Livro L
                    INNER JOIN Autor_has_Livros AHL ON L.codigo_de_barras = AHL.livro
                    INNER JOIN Autor A ON AHL.autor = A.id_autor
                """
                self.db.cursor.execute(query)
                return self.db.cursor.fetchall()
            finally:
                self.db.close()
        return []