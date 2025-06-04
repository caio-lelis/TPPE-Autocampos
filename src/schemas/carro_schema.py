# app/schemas/carro.py
from pydantic import BaseModel

from src.schemas.veiculo_schema import Veiculo

class CarroBase(BaseModel):
    num_portas: int
    vidros_eletricos: bool = False
    camera_re: bool = False
    airbags: bool = False

class CarroCreate(CarroBase):
    veiculo_id: int

class Carro(CarroBase):
    veiculo: Veiculo

    class Config:
        orm_mode = True

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        return result