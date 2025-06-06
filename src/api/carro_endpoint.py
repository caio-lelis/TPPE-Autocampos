from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.carro_schema import CarroCreate, CarroRead
from src.services import carro_service

router = APIRouter(prefix="/carros", tags=["Carros"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CarroRead)
def criar_carro(carro: CarroCreate, db: Session = Depends(get_db)):
    return carro_service.criar_carro(db, carro)

@router.get("/", response_model=list[CarroRead])
def listar_carros(db: Session = Depends(get_db)):
    return carro_service.listar_carros(db)

@router.get("/{id_carro}", response_model=CarroRead)
def buscar_carro(id_carro: int, db: Session = Depends(get_db)):
    carro = carro_service.buscar_carro_por_id(db, id_carro)
    if not carro:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return carro

@router.get("/get_by_concessionaria/{id_concessionaria}", response_model=List[CarroRead])
def get_carro_by_concessionaria(id_concessionaria: int , db: Session = Depends(get_db)):
    carros_concessionaria = carro_service.get_carro_by_concessionaria(db , id_concessionaria)
    return carros_concessionaria
