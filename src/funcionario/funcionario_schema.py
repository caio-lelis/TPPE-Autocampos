from pydantic import BaseModel, EmailStr
from decimal import Decimal
from typing import Optional

class FuncionarioBase(BaseModel):
    usuario_id: int
    rendimento_mensal: Decimal

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioUsuarioInfo(BaseModel):
    nome: str
    email: EmailStr

class FuncionarioRead(FuncionarioBase):
    id: int
    usuario: Optional[FuncionarioUsuarioInfo] = None

    class Config:
        orm_mode = True