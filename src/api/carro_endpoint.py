from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.carro_schema import CarroCreate, CarroRead
from src.services.carro_service import carro_service
from typing import List

router = APIRouter(prefix="/carros", tags=["Carros"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=CarroRead)
def create_carro_api(carro: CarroCreate, db: Session = Depends(get_db)):
    db_carro = carro_service.create_carro(db, carro)
    if not db_carro:
        raise HTTPException(status_code=400, detail="Erro ao criar carro.")
    return db_carro

@router.get("/get", response_model=List[CarroRead])
def get_all_carros_api(db: Session = Depends(get_db)):
    return carro_service.get_all_carros(db)

@router.get("/get/{carro_id}", response_model=CarroRead)
def get_carro_by_id_api(carro_id: int, db: Session = Depends(get_db)):
    db_carro = carro_service.get_carro_by_id(db, carro_id)
    if not db_carro:
        raise HTTPException(status_code=404, detail="Carro não encontrado.")
    return db_carro

@router.put("/update/{carro_id}", response_model=CarroRead)
def update_carro_api(carro_id: int, carro: CarroCreate, db: Session = Depends(get_db)):
    db_carro = carro_service.update_carro(db, carro_id, carro)
    if not db_carro:
        raise HTTPException(status_code=404, detail="Carro não encontrado.")
    return db_carro

@router.delete("/delete/{carro_id}", response_model=CarroRead)
def delete_carro_api(carro_id: int, db: Session = Depends(get_db)):
    db_carro = carro_service.delete_carro(db, carro_id)
    if not db_carro:
        raise HTTPException(status_code=404, detail="Carro não encontrado.")
    return db_carro