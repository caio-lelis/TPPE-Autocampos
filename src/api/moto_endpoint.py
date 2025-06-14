from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.moto_schema import MotoCreate, MotoRead
from src.services.moto_service import moto_service
from typing import List

router = APIRouter(prefix="/motos", tags=["Motos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=MotoRead)
def create_moto_api(moto: MotoCreate, db: Session = Depends(get_db)):
    db_moto = moto_service.create_moto(db, moto)
    if not db_moto:
        raise HTTPException(status_code=400, detail="Erro ao criar moto.")
    return db_moto

@router.get("/get", response_model=List[MotoRead])
def get_all_motos_api(db: Session = Depends(get_db)):
    return moto_service.get_all_motos(db)

@router.get("/get/{moto_id}", response_model=MotoRead)
def get_moto_by_id_api(moto_id: int, db: Session = Depends(get_db)):
    db_moto = moto_service.get_moto_by_id(db, moto_id)
    if not db_moto:
        raise HTTPException(status_code=404, detail="Moto não encontrada.")
    return db_moto

@router.put("/update/{moto_id}", response_model=MotoRead)
def update_moto_api(moto_id: int, moto: MotoCreate, db: Session = Depends(get_db)):
    db_moto = moto_service.update_moto(db, moto_id, moto)
    if not db_moto:
        raise HTTPException(status_code=404, detail="Moto não encontrada.")
    return db_moto

@router.delete("/delete/{moto_id}", response_model=MotoRead)
def delete_moto_api(moto_id: int, db: Session = Depends(get_db)):
    db_moto = moto_service.delete_moto(db, moto_id)
    if not db_moto:
        raise HTTPException(status_code=404, detail="Moto não encontrada.")
    return db_moto