# src/models/moto.py

from enum import Enum
from src.models.veiculo import Veiculo, TipoCombustivel

class TipoFreio(Enum):
    """
    Classe que representa os tipos de combustíveis disponíveis.
    """
    DISCO = "freio a disco"
    TAMBOR = "freio a tambor"
    ABS = "freio ABS"

class Moto(Veiculo):
    """
    Classe que representa uma moto, herdando da classe Veiculo.
    Adiciona atributos específicos como cilindrada, tipo de freio e se tem baú.
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
        cilindrada: int,
        torque: float,
        peso: float,
        freio: TipoFreio,
    ):
        super().__init__(id, marca, modelo, cor, ano, valor, combustivel)
        self.cilindrada = cilindrada
        self.torque = torque
        self.peso = peso
        self.tipo_freio = freio

    def __str__(self) -> str:
        return (
            f"{super().__str__()}, Moto [Cilindrada: {self.cilindrada} cc, "
            f"Torque: {self.torque} Nm, Peso: {self.peso} kg, "
            f"Tipo de Freio: {self.tipo_freio.value}]"
        )
        
if __name__ == "__main__":
    minha_moto = Moto(
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
    
    print(minha_moto)

