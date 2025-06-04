# app/schemas/comprador.py
from pydantic import BaseModel
from typing import Optional

from src.schemas.pessoa_schema import Pessoa

class CompradorBase(BaseModel):
    email: str
    renda_mensal: float
    profissao: str
    saldo_compra: Optional[float] = 0.0

class CompradorCreate(CompradorBase):
    pessoa_id: int

class Comprador(CompradorBase):
    id: int
    pessoa: Pessoa

    class Config:
        orm_mode = True

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        return result