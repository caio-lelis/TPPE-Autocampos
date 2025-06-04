# app/schemas/moto.py
from pydantic import BaseModel
from enum import Enum

from src.schemas.veiculo_schema import Veiculo

class TipoFreio(str, Enum):
    DISCO = "Disco"
    TAMBOR = "Tambor"
    ABS = "ABS"

class MotoBase(BaseModel):
    cilindradas: int
    torque: float
    peso: float
    tipo_freio: TipoFreio

class MotoCreate(MotoBase):
    veiculo_id: int

class Moto(MotoBase):
    veiculo: Veiculo

    class Config:
        orm_mode = True

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        return result