from pydantic import BaseModel, Field, ValidationError, model_validator, ConfigDict # Adicione model_validator e ConfigDict
from typing import Optional
from datetime import date

class InteresseBase(BaseModel):
    cliente_id: int
    carro_id: Optional[int] = None
    moto_id: Optional[int] = None
    data_visita: Optional[date] = None
    test_drive: Optional[bool] = False

    # --- NOVO VALIDADOR DE MODELO (Pydantic V2) ---
    # Este validador verifica ambos os campos 'carro_id' e 'moto_id' após a validação
    # de cada campo individualmente.
    @model_validator(mode='after')
    def check_vehicle_exclusivity_and_presence(self):
        # Validação de exclusividade: não pode ter carro_id E moto_id preenchidos
        if self.carro_id is not None and self.moto_id is not None:
            raise ValueError('Um interesse não pode ter carro_id e moto_id preenchidos simultaneamente.')
        
        # Validação de presença: deve ter pelo menos um carro_id OU moto_id preenchido
        if self.carro_id is None and self.moto_id is None:
            raise ValueError('Um interesse deve estar associado a um carro ou a uma moto.')
        
        return self # É essencial retornar 'self' em um model_validator(mode='after')

class InteresseCreate(InteresseBase):
    pass

class InteresseRead(InteresseBase):
    id: int

    # --- NOVA FORMA DE CONFIGURAR NO PYDANTIC V2 ---
    model_config = ConfigDict(
        from_attributes=True, # Substitui orm_mode = True
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )