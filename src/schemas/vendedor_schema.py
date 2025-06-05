from pydantic import BaseModel

class VendedorBase(BaseModel):
    nome: str
    cpf: str
    idade: int
    salario: float
    especialidade: str
    total_vendas: float

class VendedorCreate(VendedorBase):
    ...

class VendedorRead(VendedorBase):
    id_vendedor: int

    class Config:
        orm_mode = True
