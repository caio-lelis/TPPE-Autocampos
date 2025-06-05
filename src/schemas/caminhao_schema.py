from pydantic import BaseModel
from typing import Optional

class CaminhaoBase(BaseModel):
    carga: float
    tamanho: float
    tipo_carroceria: str
    num_eixos: int
    marca: str
    modelo: str
    cor: str
    ano: int
    valor: float
    tipo_combustivel: str
    fk_concessionaria_id_concessionaria: Optional[int]
    fk_comprador_id_comprador: Optional[int] = None
    fk_vendedor_id_vendedor: Optional[int] = None

class CaminhaoCreate(CaminhaoBase):
    pass

class CaminhaoRead(CaminhaoBase):
    id_caminhao: int

    class Config:
        orm_mode = True
