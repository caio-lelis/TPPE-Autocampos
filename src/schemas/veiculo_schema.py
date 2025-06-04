# app/schemas/veiculo.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum

from src.schemas.comprador_schema import Comprador
from src.schemas.concessionaria_schema import Concessionaria
from src.schemas.vendedor_schema import Vendedor

class TipoCombustivel(str, Enum):
    GASOLINA = "Gasolina"
    ALCOOL = "Álcool"
    DIESEL = "Diesel"
    FLEX = "Flex"
    ELETRICO = "Elétrico"
    HIBRIDO = "Híbrido"

class VeiculoBase(BaseModel):
    marca: str
    modelo: str
    cor: str
    ano: int
    valor: float
    tipo_combustivel: TipoCombustivel
    concessionaria_id: Optional[int] = None
    comprador_id: Optional[int] = None
    vendedor_id: Optional[int] = None

class VeiculoCreate(VeiculoBase):
    pass

class Veiculo(VeiculoBase):
    id_veiculo: int
    concessionaria: Optional[Concessionaria] = None
    comprador: Optional[Comprador] = None
    vendedor: Optional[Vendedor] = None

    class Config:
        orm_mode = True

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        return result