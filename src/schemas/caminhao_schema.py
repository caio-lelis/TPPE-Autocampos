# app/schemas/caminhao.py
from pydantic import BaseModel
from enum import Enum

from src.schemas.veiculo_schema import Veiculo

class TipoCarroceria(str, Enum):
    ABERTA = "Aberta"
    FECHADA = "Fechada"
    BAU = "Baú"
    TANQUE = "Tanque"
    GAIOLA = "Gaiola"

class CaminhaoBase(BaseModel):
    carga: float
    tamanho: float
    tipo_carroceria: TipoCarroceria
    num_eixos: int

class CaminhaoCreate(CaminhaoBase):
    veiculo_id: int

class Caminhao(CaminhaoBase):
    veiculo: Veiculo

    class Config:
        orm_mode = True

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        return result