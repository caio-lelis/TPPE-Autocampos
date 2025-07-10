from pydantic import BaseModel, EmailStr
from typing import Optional

class AdminBase(BaseModel):
    usuario_id: int
    is_admin: Optional[bool] = False

class AdminCreate(AdminBase):
    pass

class AdminUsuarioInfo(BaseModel):
    nome: str
    email: EmailStr

class AdminRead(AdminBase):
    id: int
    usuario: Optional[AdminUsuarioInfo] = None

    class Config:
        orm_mode = True