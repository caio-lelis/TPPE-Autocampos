# app/schemas/vendedor.py
from pydantic import BaseModel
from typing import Optional

from src.schemas.pessoa_schema import Pessoa

class VendedorBase(BaseModel):
    salario: float
    especialidade: str
    totalVendas: Optional[float] = 0.0

class VendedorCreate(VendedorBase):
    pessoa_id: int

class Vendedor(VendedorBase):
    id: int
    pessoa: Pessoa

    class Config:
        orm_mode = True

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        return result
