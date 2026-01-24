from domain.mixins import DescricaoMixin
import pytest


def test_mixin_implementado_corretamente():
    class EntidadeComDescricao(DescricaoMixin):
        def obter_descricao(self) -> str:
            return "Descrição teste"

    entidade = EntidadeComDescricao()
    assert entidade.obter_descricao() == "Descrição teste"


def test_mixin_nao_implementado():
    class EntidadeSemImplementacao(DescricaoMixin):
        pass

    entidade = EntidadeSemImplementacao()
    with pytest.raises(NotImplementedError):
        entidade.obter_descricao()
