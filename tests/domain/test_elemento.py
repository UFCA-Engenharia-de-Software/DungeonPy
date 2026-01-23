from domain.elemento import Elemento


def test_tem_vantagem_sobre_retorna_true_quando_ha_vantagem():
    elemento_fogo = Elemento.FOGO
    elemento_gelo = Elemento.GELO

    assert elemento_gelo.tem_vantagem_sobre(elemento_fogo) is True


def test_multiplicador_retorna_1_quando_elemento_neutro():
    elemento_neutro = Elemento.NEUTRO
    elemento_fogo = Elemento.FOGO

    assert elemento_neutro.multiplicador(elemento_fogo) == 1.0


def test_multiplicador_retorna_05_quando_ha_desvantagem():
    elemento_fogo = Elemento.FOGO
    elemento_gelo = Elemento.GELO

    assert elemento_fogo.multiplicador(elemento_gelo) == 0.5
