# app/routers/concessionaria_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.services.concessionaria_service import (
    create_concessionaria,
    get_concessionaria,
    get_concessionarias,
    update_concessionaria,
    delete_concessionaria
)

from src.db.session import SessionLocal
from src.schemas.concessionaria_schema import Concessionaria, ConcessionariaCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/concessionarias", 
             response_model=Concessionaria,
             status_code=status.HTTP_201_CREATED)
def criar_concessionaria(concessionaria: ConcessionariaCreate, db: Session = Depends(get_db)):
    try:
        return create_concessionaria(db=db, concessionaria=concessionaria)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar concessionária: {str(e)}"
        )

@router.get("/concessionarias/{concessionaria_id}", 
            response_model=Concessionaria)
def ler_concessionaria(concessionaria_id: int, db: Session = Depends(get_db)):
    db_concessionaria = get_concessionaria(db, concessionaria_id=concessionaria_id)
    if db_concessionaria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concessionária não encontrada"
        )
    return db_concessionaria

@router.get("/concessionarias", 
            response_model=List[Concessionaria])
def listar_concessionarias(db: Session = Depends(get_db)):
    return get_concessionarias(db)

@router.put("/concessionarias/{concessionaria_id}", 
            response_model=Concessionaria)
def atualizar_concessionaria(
    concessionaria_id: int, 
    concessionaria: ConcessionariaCreate, 
    db: Session = Depends(get_db)
):
    db_concessionaria = update_concessionaria(
        db, 
        concessionaria_id=concessionaria_id, 
        concessionaria=concessionaria
    )
    if db_concessionaria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concessionária não encontrada"
        )
    return db_concessionaria

@router.delete("/concessionarias/{concessionaria_id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def remover_concessionaria(concessionaria_id: int, db: Session = Depends(get_db)):
    success = delete_concessionaria(db, concessionaria_id=concessionaria_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concessionária não encontrada"
        )