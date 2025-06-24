from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class MotoBase(BaseModel):
    modelo: str
    marca: str
    ano: int = Field(..., gt=1900, lt=2100)
    cor: Optional[str] = None
    tipo_combustivel: Optional[str] = None
    preco: Decimal = Field(..., gt=0)
    revisado: Optional[bool] = False
    disponivel: Optional[bool] = True
    freio_dianteiro: Optional[str] = None
    freio_traseiro: Optional[str] = None
    estilo: Optional[str] = None
    cilindradas: Optional[int] = Field(None, gt=0)
    velocidade_max: Optional[int] = Field(None, gt=0)

class MotoCreate(MotoBase):
    pass

class MotoRead(MotoBase):
    id: int

    class Config:
        orm_mode = True