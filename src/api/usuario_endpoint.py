from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.usuario_schema import UsuarioCreate, UsuarioRead
from src.services.usuario_service import usuario_service # Importa a instância do serviço
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=UsuarioRead)
def create_usuario_api(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = usuario_service.create_usuario(db, usuario)
    if not db_usuario:
        raise HTTPException(status_code=400, detail="Erro ao criar usuário.")
    return db_usuario

@router.get("/get", response_model=List[UsuarioRead])
def get_all_usuarios_api(db: Session = Depends(get_db)):
    return usuario_service.get_all_usuarios(db)

@router.get("/get/{usuario_id}", response_model=UsuarioRead)
def get_usuario_by_id_api(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = usuario_service.get_usuario_by_id(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_usuario

@router.put("/update/{usuario_id}", response_model=UsuarioRead)
def update_usuario_api(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = usuario_service.update_usuario(db, usuario_id, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_usuario

@router.delete("/delete/{usuario_id}", response_model=UsuarioRead)
def delete_usuario_api(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = usuario_service.delete_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_usuario