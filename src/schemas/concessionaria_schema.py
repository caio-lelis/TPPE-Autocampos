# app/schemas/concessionaria.py
from pydantic import BaseModel, validator
from typing import Optional

class ConcessionariaBase(BaseModel):
    nome: str
    endereco: str
    cnpj: str
    telefone: str

class ConcessionariaCreate(ConcessionariaBase):
    pass

class Concessionaria(ConcessionariaBase):
    id_concessionaria: int

    class Config:
        orm_mode = True

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        return result