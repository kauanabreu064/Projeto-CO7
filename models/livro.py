class Livro:
    def __init__(self, codigo_de_barras, nome, publicacao, valor_reposicao):
        self.codigo_de_barras = codigo_de_barras
        self.nome = nome
        self.publicacao = publicacao
        self.valor_reposicao = valor_reposicao

    def __str__(self):
        return f"Livro: {self.nome} (Código: {self.codigo_de_barras})"
