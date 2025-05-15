# src/models/veiculo.py

from enum import Enum
from typing import Optional

class TipoCombustivel(Enum):
    """
    Classe que representa os tipos de combustíveis disponíveis.
    """
    GASOLINA = "Gasolina"
    ETANOL = "Etanol"
    DIESEL = "Diesel"
    FLEX = "Flex"
    
class Veiculo:
    """
    Classe base Veiculo.
    Representa um veículo com atributos como marca, modelo, cor, ano,
    valor e tipo de combustível.
    """
    def __init__(
        self,
        id: int,
        marca: str,
        modelo: str,
        cor: str,
        ano: int,
        valor: float,
        combustivel: TipoCombustivel
    ):
        self.id = id
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.ano = ano
        self.valor = valor
        self.combustivel = combustivel

    def __str__(self) -> str:
        return (
            f"Veículo [ID: {self.id}, Marca: {self.marca}, Modelo: {self.modelo}, "
            f"Cor: {self.cor}, Ano: {self.ano}, Valor: R${self.valor:.2f}, "
            f"Combustível: {self.combustivel.value}]"
        )