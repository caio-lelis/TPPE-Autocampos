
from typing import Optional
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



class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None

    class Config:
        orm_mode = True