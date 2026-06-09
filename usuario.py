class Usuario:
    def __init__(self, matricula, nome, telefone, data_nasc, cartao_acesso):
        self.matricula = matricula
        self.nome = nome
        self.telefone = telefone
        self.data_nasc = data_nasc
        self.cartao_acesso = cartao_acesso

    def __str__(self):
        return f"Usuário: {self.nome} (Matrícula: {self.matricula})"