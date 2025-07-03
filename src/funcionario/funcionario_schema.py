from pydantic import BaseModel
from decimal import Decimal

class FuncionarioBase(BaseModel):
    usuario_id: int
    rendimento_mensal: Decimal

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioRead(FuncionarioBase):
    id: int

    class Config:
        orm_mode = True