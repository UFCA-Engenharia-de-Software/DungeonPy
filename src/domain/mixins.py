class DescricaoMixin:
    """
    Mixin que define o contrato para classes que possuem
    uma descrição textual.

    Classes que herdam deste mixin devem obrigatoriamente
    implementar o método `obter_descricao`.
    """

    def obter_descricao(self) -> str:
        raise NotImplementedError("A classe deve implementar obter_descricao()")
