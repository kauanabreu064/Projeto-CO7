import funcoes_banco


def menu():
    print("===================================")
    print("   SISTEMA DA BIBLIOTECA INICIADO  ")
    print("===================================")

    funcoes_banco.listar_livros()

    funcoes_banco.listar_usuarios()

    print("\n===================================")
    print(" Teste de integração finalizado!   ")
    print("===================================")


if __name__ == "__main__":
    menu()