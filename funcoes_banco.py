from conexao import criar_conexao
from mysql.connector import Error


def listar_livros():
    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT codigo_de_barras, nome, publicacao, valor_reposicao FROM Livro;")
            livros = cursor.fetchall()

            print("\n--- CATÁLOGO DE LIVROS ---")
            for livro in livros:
                print(
                    f"[{livro['codigo_de_barras']}] {livro['nome']} (Publicado em: {livro['publicacao']}) - R$ {livro['valor_reposicao']:.2f}")

        except Error as e:
            print(f"Erro ao buscar livros: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()


def listar_usuarios():
    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT matricula, nome, telefone FROM Usuario;")
            usuarios = cursor.fetchall()

            print("\n--- USUÁRIOS CADASTRADOS ---")
            for user in usuarios:
                print(f"Matrícula: {user['matricula']} | Nome: {user['nome']} | Tel: {user['telefone']}")

        except Error as e:
            print(f"Erro ao buscar usuários: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()