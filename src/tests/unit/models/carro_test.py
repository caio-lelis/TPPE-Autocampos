# Corrija o arquivo src/tests/unit/models/carro_test.py
import unittest
from src.models.veiculo import TipoCombustivel
from src.models.carro import Carro

class TestCarro(unittest.TestCase):
    def setUp(self):
        self.carro = Carro(
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
    
    def test_criacao_carro(self):
        self.assertIsInstance(self.carro, Carro)

# Adicione isso no final do arquivo
if __name__ == '__main__':
    unittest.main()