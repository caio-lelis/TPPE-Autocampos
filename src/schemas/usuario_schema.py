from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nome: str
    cpf: str
    email: EmailStr
    senha: str # Em um ambiente real, a senha não deveria ser exposta diretamente em um schema de leitura.

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioRead(BaseModel):
    id: int
    nome: str
    cpf: str
    email: EmailStr

    class Config:
        orm_mode = True