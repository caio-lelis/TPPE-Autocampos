import pytest
from src.models.veiculo import TipoCombustivel
from src.models.carro import Carro

@pytest.fixture
def carro():
    return Carro(
id=1,
marca="Toyota",
modelo="Corolla",
cor="Prata",
ano=2022,
valor=120000.00,
combustivel=TipoCombustivel.FLEX,
num_portas=4,
vidro_eletrico=True,
airbag=True,
camera_re=True
)

@pytest.mark.skip(reason="Teste de criação de carro")
def test_criacao_carro(carro):
    assert isinstance(carro, Carro)

@pytest.mark.skip(reason="Teste de string do carro")
def test_atributos_carro(carro):
    assert carro.marca == "Toyota"
    assert carro.modelo == "Corolla"
    assert carro.cor == "Prata"
    assert carro.ano == 2022
    assert carro.valor == 120000.00
    assert carro.combustivel == TipoCombustivel.FLEX
    assert carro.num_portas == 4
    assert carro.vidro_eletrico is True
    assert carro.airbag is True
    assert carro.camera_re is True