from pydantic import BaseModel

class CompradorBase(BaseModel):
    nome: str
    cpf: str
    idade: int
    email: str
    renda_mensal: float
    profissao: str
    saldo_compra: float

class CompradorCreate(CompradorBase):
    ...

class CompradorRead(CompradorBase):
    id_comprador: int

    class Config:
        orm_mode = True
