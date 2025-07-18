from pydantic import BaseModel, HttpUrl, ValidationError, FieldValidationInfo, field_validator, model_validator, ConfigDict
from typing import Optional, Union
from datetime import date

class AnuncioBase(BaseModel):
    funcionario_id: Optional[int] = None
    carro_id: Optional[int] = None
    moto_id: Optional[int] = None
    data_publicacao: Optional[date] = date.today()
    imagem1_url: Optional[Union[HttpUrl, str]] = None
    imagem2_url: Optional[Union[HttpUrl, str]] = None
    imagem3_url: Optional[Union[HttpUrl, str]] = None

    @model_validator(mode='after')
    def check_carro_moto_exclusivity_and_at_least_one_vehicle(self):
        if self.carro_id is not None and self.moto_id is not None:
            raise ValueError('Um anúncio não pode ter carro_id e moto_id preenchidos simultaneamente.')
        
        if self.carro_id is None and self.moto_id is None:
            raise ValueError('Um anúncio deve estar associado a um carro ou a uma moto.')
        
        return  self
class AnuncioCreate(AnuncioBase):
    pass

class AnuncioRead(AnuncioBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True, 
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )