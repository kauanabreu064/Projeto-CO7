from daos.usuario_dao import UsuarioDAO
from daos.livro_dao import LivroDAO
from daos.emprestimo_dao import EmprestimoDAO
from daos.cartao_dao import CartaoDAO
from daos.autor_dao import AutorDAO


def menu_usuarios(usuario_dao):
    while True:
        print("\n=== GERENCIAR USUÁRIOS ===")
        print("1. Cadastrar Usuário")
        print("2. Listar Todos os Usuários")
        print("3. Atualizar Dados do Usuário")
        print("4. Remover Usuário")
        print("5. Buscar Usuário por Nome")
        print("6. Ver Detalhes do Usuário + Cartão")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n[Novo Usuário]")
            matricula = int(input("Matrícula: "))
            nome = input("Nome Completo: ")
            telefone = input("Telefone (11 dígitos): ")
            data_nasc = input("Data de Nascimento (AAAA-MM-DD): ")
            cartao = int(input("Código de Barras do Cartão de Acesso: "))
            usuario_dao.insert(matricula, nome, telefone, data_nasc, cartao)

        elif opcao == '2':
            usuarios = usuario_dao.get_all()
            print("\n--- LISTA DE USUÁRIOS ---")
            for u in usuarios:
                print(f"Matrícula: {u['matricula']} | Nome: {u['nome']} | Tel: {u['telefone']}")

        elif opcao == '3':
            matricula = int(input("\nDigite a matrícula do usuário a atualizar: "))
            novo_nome = input("Novo Nome: ")
            novo_tel = input("Novo Telefone: ")
            usuario_dao.update(matricula, novo_nome, novo_tel)

        elif opcao == '4':
            matricula = int(input("\nDigite a matrícula do usuário a remover: "))
            usuario_dao.delete(matricula)

        elif opcao == '5':
            nome_busca = input("\nDigite o nome (ou parte dele) para buscar: ")
            resultados = usuario_dao.search_by_nome(nome_busca)
            print("\n--- RESULTADOS DA BUSCA ---")
            for u in resultados:
                print(f"Matrícula: {u['matricula']} | Nome: {u['nome']} | Tel: {u['telefone']}")

        elif opcao == '6':
            matricula = int(input("\nDigite a matrícula para ver detalhes com o Cartão: "))
            res = usuario_dao.get_usuario_com_cartao(matricula)
            if res:
                print("\n--- DETALHES DO USUÁRIO + CARTÃO ---")
                print(f"Usuário: {res['nome']} (Matrícula: {res['matricula']})")
                print(f"Cartão de Acesso: {res['codigo_de_barras']} | Emitido em: {res['data_emissao']}")
                print(f"Status do Cartão: {'ATIVO' if res['esta_ativo'] == 1 else 'INATIVO'}")
            else:
                print("Usuário ou cartão não encontrado no banco.")

        elif opcao == '0':
            break
        else:
            print("Opção inválida!")


def menu_livros(livro_dao):
    while True:
        print("\n=== GERENCIAR LIVROS ===")
        print("1. Cadastrar Livro")
        print("2. Listar Todos os Livros")
        print("3. Atualizar Valor do Livro")
        print("4. Remover Livro (DELETE)")
        print("5. Buscar Livro por Título")
        print("6. Ver Catálogo de Livros e seus Autores")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n[Novo Livro]")
            codigo = int(input("Código de Barras: "))
            nome = input("Título do Livro: ")
            publicacao = input("Data de Publicação (AAAA-MM-DD): ")
            valor = float(input("Valor de Reposição: R$ "))
            livro_dao.insert(codigo, nome, publicacao, valor)

        elif opcao == '2':
            livros = livro_dao.get_all()
            print("\n--- CATÁLOGO DE LIVROS ---")
            for l in livros:
                print(f"[{l['codigo_de_barras']}] {l['nome']} - Valor Reposição: R$ {l['valor_reposicao']:.2f}")

        elif opcao == '3':
            codigo = int(input("\nDigite o código de barras do livro: "))
            novo_valor = float(input("Novo Valor de Reposição: R$ "))
            livro_dao.update_valor(codigo, novo_valor)

        elif opcao == '4':
            codigo = int(input("\nDigite o código de barras do livro a remover: "))
            livro_dao.delete(codigo)

        elif opcao == '5':
            titulo_busca = input("\nDigite o título (ou parte dele) para buscar: ")
            resultados = livro_dao.search_by_titulo(titulo_busca)
            print("\n--- RESULTADOS DA BUSCA ---")
            for l in resultados:
                print(f"[{l['codigo_de_barras']}] {l['nome']} - R$ {l['valor_reposicao']:.2f}")

        elif opcao == '6':
            resultados = livro_dao.get_livros_com_autores()
            print("\n--- LIVROS E AUTORES ASSOCIADOS ---")
            for r in resultados:
                print(f"Livro: {r['livro']} [{r['codigo_de_barras']}] | Autor: {r['autor']} ({r['nacionalidade']})")

        elif opcao == '0':
            break
        else:
            print("Opção inválida!")


def menu_emprestimos(emprestimo_dao):
    while True:
        print("\n=== GERENCIAR EMPRÉSTIMOS ===")
        print("1. Registrar Novo Empréstimo")
        print("2. Listar Todos os Empréstimos")
        print("3. Registrar Devolução de Livro")
        print("4. Remover Registro de Empréstimo")
        print("5. Buscar Empréstimos por Aluno")
        print("6. Ver Relatório de Empréstimos + Alunos")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n[Novo Empréstimo]")
            data_retirada = input("Data de Retirada (AAAA-MM-DD): ")
            data_prevista = input("Data de Devolução Prevista (AAAA-MM-DD): ")
            usuario_id = int(input("Matrícula do Aluno que está pegando o livro: "))
            emprestimo_dao.insert(data_retirada, data_prevista, usuario_id)

        elif opcao == '2':
            emprestimos = emprestimo_dao.get_all()
            print("\n--- HISTÓRICO DE EMPRÉSTIMOS ---")
            for e in emprestimos:
                status = "DEVOLVIDO" if e['foi_devolvido'] == 1 else "PENDENTE"
                print(f"ID Empréstimo: {e['id_emprestimo']} | Aluno (Matrícula): {e['usuario']} | Status: {status}")

        elif opcao == '3':
            id_emp = int(input("\nDigite o ID do Empréstimo para confirmar a devolução: "))
            emprestimo_dao.registrar_devolucao(id_emp)

        elif opcao == '4':
            id_emp = int(input("\nDigite o ID do Empréstimo a ser deletado: "))
            emprestimo_dao.delete(id_emp)

        elif opcao == '5':
            matricula = int(input("\nDigite a matrícula do aluno para buscar os empréstimos dele: "))
            resultados = emprestimo_dao.search_by_usuario_id(matricula)
            print("\n--- RESULTADOS DA BUSCA ---")
            for e in resultados:
                status = "DEVOLVIDO" if e['foi_devolvido'] == 1 else "PENDENTE"
                print(f"ID Empréstimo: {e['id_emprestimo']} | Retirado em: {e['data_retirada']} | Status: {status}")

        elif opcao == '6':
            resultados = emprestimo_dao.get_emprestimos_com_usuarios()
            print("\n--- EMPRÉSTIMOS E DADOS DOS ALUNOS ---")
            for r in resultados:
                status = "DEVOLVIDO" if r['foi_devolvido'] == 1 else "PENDENTE"
                print(f"ID: {r['id_emprestimo']} | Aluno: {r['nome']} | Tel: {r['telefone']} | Status: {status}")

        elif opcao == '0':
            break
        else:
            print("Opção inválida!")


def menu_cartoes(cartao_dao):
    while True:
        print("\n=== GERENCIAR CARTÕES DE ACESSO ===")
        print("1. Cadastrar Novo Cartão")
        print("2. Listar Todos os Cartões")
        print("3. Atualizar Status do Cartão")
        print("4. Remover Cartão")
        print("5. Buscar Cartão por Código")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n[Novo Cartão]")
            codigo = int(input("Código de Barras do Cartão: "))
            data_emissao = input("Data de Emissão (AAAA-MM-DD): ")
            status = int(input("Status (1 para Ativo, 0 para Inativo): "))
            cartao_dao.insert(codigo, data_emissao, status)

        elif opcao == '2':
            cartoes = cartao_dao.get_all()
            print("\n--- LISTA DE CARTÕES ---")
            for c in cartoes:
                status = "ATIVO" if c['esta_ativo'] == 1 else "INATIVO"
                print(f"Código: {c['codigo_de_barras']} | Emissão: {c['data_emissao']} | Status: {status}")

        elif opcao == '3':
            codigo = int(input("\nDigite o código de barras do cartão: "))
            novo_status = int(input("Novo Status (1 para Ativo, 0 para Inativo): "))
            cartao_dao.update_status(codigo, novo_status)

        elif opcao == '4':
            codigo = int(input("\nDigite o código de barras do cartão a ser deletado: "))
            cartao_dao.delete(codigo)

        elif opcao == '5':
            codigo = int(input("\nDigite o código do cartão para buscar: "))
            resultados = cartao_dao.search_by_codigo(codigo)
            print("\n--- RESULTADOS DA BUSCA ---")
            for c in resultados:
                status = "ATIVO" if c['esta_ativo'] == 1 else "INATIVO"
                print(f"Código: {c['codigo_de_barras']} | Emissão: {c['data_emissao']} | Status: {status}")

        elif opcao == '0':
            break
        else:
            print("Opção inválida!")


def menu_autores(autor_dao):
    while True:
        print("\n=== GERENCIAR AUTORES ===")
        print("1. Cadastrar Novo Autor")
        print("2. Listar Todos os Autores")
        print("3. Atualizar Dados do Autor")
        print("4. Remover Autor")
        print("5. Buscar Autor por Nome")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n[Novo Autor]")
            nome = input("Nome do Autor: ")
            nac = input("Nacionalidade: ")
            data_nasc = input("Data de Nascimento (AAAA-MM-DD): ")
            autor_dao.insert(nome, nac, data_nasc)

        elif opcao == '2':
            autores = autor_dao.get_all()
            print("\n--- LISTA DE AUTORES ---")
            for a in autores:
                print(f"ID: {a['id_autor']} | Nome: {a['nome']} | Nacionalidade: {a['nacionalidade']}")

        elif opcao == '3':
            id_autor = int(input("\nDigite o ID do autor: "))
            novo_nome = input("Novo Nome: ")
            nova_nac = input("Nova Nacionalidade: ")
            autor_dao.update(id_autor, novo_nome, nova_nac)

        elif opcao == '4':
            id_autor = int(input("\nDigite o ID do autor a ser deletado: "))
            autor_dao.delete(id_autor)

        elif opcao == '5':
            nome_busca = input("\nDigite o nome (ou parte) para buscar: ")
            resultados = autor_dao.search_by_nome(nome_busca)
            print("\n--- RESULTADOS DA BUSCA ---")
            for a in resultados:
                print(f"ID: {a['id_autor']} | Nome: {a['nome']} | Nacionalidade: {a['nacionalidade']}")

        elif opcao == '0':
            break
        else:
            print("Opção inválida!")

def relatorio_geral(usuario_dao, livro_dao, emprestimo_dao, cartao_dao, autor_dao):
    print("\n" + "="*50)
    print("   RAIO-X DO BANCO DE DADOS (SELECT * GERAL)")
    print("="*50)
    
    print("\n--- 1. TABELA DE USUÁRIOS ---")
    usuarios = usuario_dao.get_all()
    for u in usuarios:
        print(f"Matrícula: {u['matricula']} | Nome: {u['nome']} | Tel: {u['telefone']}")
        
    print("\n--- 2. TABELA DE LIVROS ---")
    livros = livro_dao.get_all()
    for l in livros:
        print(f"[{l['codigo_de_barras']}] {l['nome']} - R$ {l['valor_reposicao']:.2f}")
        
    print("\n--- 3. TABELA DE EMPRÉSTIMOS ---")
    emprestimos = emprestimo_dao.get_all()
    for e in emprestimos:
        status = "DEVOLVIDO" if e['foi_devolvido'] == 1 else "PENDENTE"
        print(f"ID: {e['id_emprestimo']} | Aluno: {e['usuario']} | Status: {status}")
        
    print("\n--- 4. TABELA DE CARTÕES DE ACESSO ---")
    cartoes = cartao_dao.get_all()
    for c in cartoes:
        status = "ATIVO" if c['esta_ativo'] == 1 else "INATIVO"
        print(f"Código: {c['codigo_de_barras']} | Emissão: {c['data_emissao']} | Status: {status}")
        
    print("\n--- 5. TABELA DE AUTORES ---")
    autores = autor_dao.get_all()
    for a in autores:
        print(f"ID: {a['id_autor']} | Nome: {a['nome']} | Nac: {a['nacionalidade']}")
        
    print("\n" + "="*50)

def main():
    usuario_dao = UsuarioDAO()
    livro_dao = LivroDAO()
    emprestimo_dao = EmprestimoDAO()
    cartao_dao = CartaoDAO()
    autor_dao = AutorDAO()

    while True:
        print("\n=======================================")
        print("     SISTEMA DA BIBLIOTECA - PRINCIPAL  ")
        print("=======================================")
        print("1. Menu de Gerenciamento de Usuários")
        print("2. Menu de Gerenciamento de Livros")
        print("3. Menu de Gerenciamento de Empréstimos")
        print("4. Menu de Gerenciamento de Cartões de Acesso")
        print("5. Menu de Gerenciamento de Autores")
        print("6. Mostrar Todo o Banco de Dados")
        print("0. Sair do Sistema")
        print("=======================================")

        opcao = input("Escolha o submenu que deseja acessar: ")

        if opcao == '1':
            menu_usuarios(usuario_dao)
        elif opcao == '2':
            menu_livros(livro_dao)
        elif opcao == '3':
            menu_emprestimos(emprestimo_dao)
        elif opcao == '4':
            menu_cartoes(cartao_dao)
        elif opcao == '5':
            menu_autores(autor_dao)
        elif opcao == '6':
            relatorio_geral(usuario_dao, livro_dao, emprestimo_dao, cartao_dao, autor_dao)
        elif opcao == '0':
            print("\nEncerrando o sistema da biblioteca. Até à próxima!")
            break
        else:
            print("Opção incorreta! Digite um número entre 0 e 5.")


if __name__ == "__main__":
    main()
