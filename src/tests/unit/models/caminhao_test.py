# tests/test_caminhao.py

import pytest
from src.models.veiculo import TipoCombustivel
from src.models.caminhao import Caminhao


@pytest.fixture
def caminhao_volvo():
    return Caminhao(
        id=1,
        marca="Volvo",
        modelo="FH",
        cor="Branco",
        ano=2022,
        valor=450000.00,
        combustivel=TipoCombustivel.DIESEL,
        carga=30000,
        tamanho=12.5,
        numEixos=4,
        tipoCarroceria="Baú"
    )


@pytest.fixture
def caminhao_scania():
    return Caminhao(
        id=2,
        marca="Scania",
        modelo="R500",
        cor="Azul",
        ano=2023,
        valor=520000.00,
        combustivel=TipoCombustivel.DIESEL,
        carga=32000,
        tamanho=13.0,
        numEixos=5,
        tipoCarroceria="Graneleiro"
    )


@pytest.mark.skip(reason="Teste de criação de caminhão")
def test_criacao_caminhao(caminhao_volvo):
    assert caminhao_volvo.id == 1
    assert caminhao_volvo.marca == "Volvo"
    assert caminhao_volvo.modelo == "FH"
    assert caminhao_volvo.cor == "Branco"
    assert caminhao_volvo.ano == 2022
    assert caminhao_volvo.valor == 450000.00
    assert caminhao_volvo.combustivel == TipoCombustivel.DIESEL

    assert caminhao_volvo.carga == 30000
    assert caminhao_volvo.tamanho == 12.5
    assert caminhao_volvo.numEixos == 4
    assert caminhao_volvo.tipoCarroceria == "Baú"


@pytest.mark.skip(reason="Teste de string do caminhão")
def test_str_caminhao(caminhao_scania):
    resultado_str = str(caminhao_scania)
    assert "Scania" in resultado_str
    assert "R500" in resultado_str
    assert "Graneleiro" in resultado_str
    assert "Eixos: 5" in resultado_str
    assert "Carga: 32000" in resultado_str