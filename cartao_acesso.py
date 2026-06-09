class CartaoAcesso:
    def __init__(self, codigo_de_barras, data_emissao, esta_ativo=1):
        self.codigo_de_barras = codigo_de_barras
        self.data_emissao = data_emissao
        self.esta_ativo = esta_ativo

    def __str__(self):
        status = "Ativo" if self.esta_ativo == 1 else "Inativo"
        return f"Cartão: {self.codigo_de_barras} (Emitido em: {self.data_emissao}) - Status: {status}"