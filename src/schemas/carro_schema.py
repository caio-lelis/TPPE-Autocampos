from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class CarroBase(BaseModel):
    modelo: str
    marca: str
    ano: int = Field(..., gt=1900, lt=2100)
    cor: Optional[str] = None
    tipo_combustivel: Optional[str] = None
    preco: Decimal = Field(..., gt=0)
    revisado: Optional[bool] = False
    disponivel: Optional[bool] = True
    tipo_direcao: Optional[str] = None
    tracao: Optional[str] = None
    consumo_cidade: Optional[Decimal] = None
    airbag: Optional[bool] = False
    ar_condicionado: Optional[bool] = False

class CarroCreate(CarroBase):
    pass

class CarroRead(CarroBase):
    id: int

    class Config:
        orm_mode = True