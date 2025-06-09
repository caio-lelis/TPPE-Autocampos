from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.moto_schema import MotoCreate, MotoRead
from src.services import moto_service

router = APIRouter(prefix="/motos", tags=["Motos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=MotoRead)
def post_moto(moto: MotoCreate, db: Session = Depends(get_db)):
    return moto_service.create_moto(db, moto)

@router.get("/get_all", response_model=list[MotoRead])
def get_all(db: Session = Depends(get_db)):
    return moto_service.get_all_motos(db)

@router.get("/get_by_id/{id_moto}", response_model=MotoRead)
def buscar_moto(id_moto: int, db: Session = Depends(get_db)):
    moto = moto_service.get_moto_by_id(db, id_moto)
    if not moto:
        raise HTTPException(status_code=404, detail="Moto não encontrada")
    return moto

@router.get("/get_by_concessionaria/{id_concessionaria}", response_model=List[MotoRead] , 
            summary="Obtém motos de uma determinada concessionária",
            description="Caso a concessionaria exista, retorna uma lista com todas as motos desta concessionária")
def get_moto_by_concessionaria(id_concessionaria: int , db: Session = Depends(get_db)):
    motos_concessionaria = moto_service.get_moto_by_concessionaria(db , id_concessionaria)
    return motos_concessionaria