from pydantic import BaseModel
from typing import Optional

class MotoBase(BaseModel):
    cilindradas: int
    torque: float
    peso: float
    tipo_freio: str
    marca: str
    modelo: str
    cor: str
    ano: int
    valor: float
    tipo_combustivel: str
    fk_concessionaria_id_concessionaria: Optional[int]
    fk_comprador_id_comprador: Optional[int] = None
    fk_vendedor_id_vendedor: Optional[int] = None

class MotoCreate(MotoBase):
    pass

class MotoRead(MotoBase):
    id_moto: int

    class Config:
        orm_mode = True
