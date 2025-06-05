from pydantic import BaseModel

class ConcessionariaBase(BaseModel):
    nome: str
    endereco: str
    cnpj: str
    telefone: str

class ConcessionariaCreate(ConcessionariaBase):
    pass

class ConcessionariaRead(ConcessionariaBase):
    id_concessionaria: int

    class Config:
        orm_mode = True
