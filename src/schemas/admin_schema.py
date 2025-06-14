from pydantic import BaseModel
from typing import Optional

class AdminBase(BaseModel):
    usuario_id: int
    is_admin: Optional[bool] = False

class AdminCreate(AdminBase):
    pass

class AdminRead(AdminBase):
    id: int

    class Config:
        orm_mode = True