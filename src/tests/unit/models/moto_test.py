# tests/test_moto.py

import pytest
from src.models.veiculo import TipoCombustivel
from src.models.moto import Moto, TipoFreio

@pytest.fixture
def moto():
    return Moto(
        id=1,
        marca="Honda",
        modelo="CB 500F",
        cor="Vermelha",
        ano=2023,
        valor=35000.00,
        combustivel=TipoCombustivel.GASOLINA,
        cilindrada=500,
        torque=4.5,
        peso=180.0,
        freio=TipoFreio.ABS
    )

@pytest.mark.skip(reason="Teste de criação de moto")
def test_criacao_moto(moto):
    assert isinstance(moto, Moto)

@pytest.mark.skip(reason="Teste de string da moto")
def test_atributos_herdados(moto):
    assert moto.marca == "Honda"
    assert moto.modelo == "CB 500F"
    assert moto.ano == 2023
    assert moto.combustivel == TipoCombustivel.GASOLINA

@pytest.mark.skip(reason="Teste de string da moto")
def test_atributos_especificos_moto(moto):
    assert moto.cilindrada == 500
    assert moto.torque == 4.5
    assert moto.peso == 180.0
    assert moto.tipo_freio == TipoFreio.ABS

@pytest.mark.skip(reason="Teste de string da moto")
def test_str_moto(moto):
    resultado = str(moto)
    assert "CB 500F" in resultado
    assert "500 cc" in resultado
    assert "freio ABS" in resultado
