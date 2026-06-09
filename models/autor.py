class Autor:
    def __init__(self, nome, nacionalidade, data_nasc, id_autor=None):
        self.id_autor = id_autor
        self.nome = nome
        self.nacionalidade = nacionalidade
        self.data_nasc = data_nasc

    def __str__(self):
        return f"Autor: {self.nome} ({self.nacionalidade})"
