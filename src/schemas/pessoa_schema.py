# app/schemas/pessoa.py
from pydantic import BaseModel
from typing import Optional

class PessoaBase(BaseModel):
    nome: str
    cpf: str
    idade: Optional[int] = None

class PessoaCreate(PessoaBase):
    pass

class Pessoa(PessoaBase):
    id: int

    class Config:
        orm_mode = True

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        return result