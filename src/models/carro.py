# src/models/carro.py

from src.models.veiculo import Veiculo
from src.models.veiculo import TipoCombustivel
# from veiculo import Veiculo
# from veiculo import TipoCombustivel
from typing import Optional


class Carro(Veiculo):
    """
    Classe Carro que herda de Veiculo.
    Representa um carro com atributos adicionais como número de portas,
    se possui vidro elétrico, airbag e câmera de ré.
    """
    def __init__(
        self,
        id: int,
        marca: str,
        modelo: str,
        cor: str,
        ano: int,
        valor: float,
        combustivel: TipoCombustivel,
        num_portas: int,
        vidro_eletrico: bool,
        airbag: bool,
        camera_re: bool
    ):
        super().__init__(id, marca, modelo, cor, ano, valor, combustivel)
        
        self.num_portas = num_portas
        self.vidro_eletrico = vidro_eletrico
        self.airbag = airbag
        self.camera_re = camera_re

    def __str__(self) -> str:
        veiculo_info = super().__str__().replace("Veículo", "Carro")
        return (
            f"{veiculo_info}, "
            f"Portas: {self.num_portas}, Vidro Elétrico: {'Sim' if self.vidro_eletrico else 'Não'}, "
            f"Airbag: {'Sim' if self.airbag else 'Não'}, Câmera Ré: {'Sim' if self.camera_re else 'Não'}"
        )

if __name__ == "__main__":
    meu_carro = Carro(
        id=1,
        marca="Ford",
        modelo="Fiesta",
        cor="Prata",
        ano=2020,
        valor=45000.00,
        combustivel=TipoCombustivel.FLEX,
        num_portas=4,
        vidro_eletrico=True,
        airbag=True,
        camera_re=False
    )
    
    print(meu_carro)