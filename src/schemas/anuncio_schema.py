from pydantic import BaseModel, HttpUrl, ValidationError, FieldValidationInfo, field_validator, model_validator, ConfigDict
from typing import Optional, Union
from datetime import date

class AnuncioBase(BaseModel):
    funcionario_id: int
    carro_id: Optional[int] = None
    moto_id: Optional[int] = None
    data_publicacao: Optional[date] = date.today()
    imagem1_url: Optional[HttpUrl] = None
    imagem2_url: Optional[HttpUrl] = None
    imagem3_url: Optional[HttpUrl] = None

    # --- NOVO VALIDADOR PARA EXCLUSIVIDADE (Pydantic V2) ---
    # Usaremos @model_validator para verificar ambos os campos após a validação de todos eles.
    # O Pydantic V2 prefere que a lógica de validação que depende de múltiplos campos
    # seja feita em um model_validator.
    @model_validator(mode='after') # 'after' executa após a validação dos campos individuais
    def check_carro_moto_exclusivity_and_at_least_one_vehicle(self):
        if self.carro_id is not None and self.moto_id is not None:
            raise ValueError('Um anúncio não pode ter carro_id e moto_id preenchidos simultaneamente.')
        
        if self.carro_id is None and self.moto_id is None:
            raise ValueError('Um anúncio deve estar associado a um carro ou a uma moto.')
        
        return self # Retorne a instância do modelo

class AnuncioCreate(AnuncioBase):
    pass

class AnuncioRead(AnuncioBase):
    id: int

    # --- NOVA FORMA DE CONFIGURAR NO PYDANTIC V2 ---
    model_config = ConfigDict(
        from_attributes=True, # Substitui orm_mode = True
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )