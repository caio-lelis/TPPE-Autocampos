from pydantic import BaseModel
from typing import Optional

class CarroBase(BaseModel):
    num_portas: int
    vidros_eletricos: bool
    camera_re: bool
    airbags: bool
    status_carro: bool
    marca: str
    modelo: str
    cor: str
    ano: int
    valor: float
    tipo_combustivel: str
    fk_concessionaria_id_concessionaria: Optional[int]
    fk_comprador_id_comprador: Optional[int] = None
    fk_vendedor_id_vendedor: Optional[int] = None

class CarroCreate(CarroBase):
    pass

class CarroRead(CarroBase):
    id_carro: int

    class Config:
        orm_mode = True
