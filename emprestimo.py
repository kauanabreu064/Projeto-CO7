
class Emprestimo:
    def __init__(self, data_retirada, data_devolucao_prevista, usuario, multa=0.0, foi_devolvido=0, id_emprestimo=None):
        self.id_emprestimo = id_emprestimo
        self.data_retirada = data_retirada
        self.data_devolucao_prevista = data_devolucao_prevista
        self.multa = multa
        self.foi_devolvido = foi_devolvido
        self.usuario = usuario  # Recebe a matrícula do usuário

    def __str__(self):
        status = "Devolvido" if self.foi_devolvido == 1 else "Pendente"
        return f"Empréstimo ID {self.id_emprestimo} - Aluno: {self.usuario} - Status: {status}"