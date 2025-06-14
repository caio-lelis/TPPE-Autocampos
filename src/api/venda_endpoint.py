from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.venda_schema import VendaCreate, VendaRead
from src.services.venda_service import venda_service
from typing import List

router = APIRouter(prefix="/vendas", tags=["Vendas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=VendaRead)
def create_venda_api(venda: VendaCreate, db: Session = Depends(get_db)):
    try:
        db_venda = venda_service.create_venda(db, venda)
    except ValueError as e: # Captura a exceção de validação do Pydantic/Service
        raise HTTPException(status_code=400, detail=str(e))
    if not db_venda:
        raise HTTPException(status_code=400, detail="Erro ao criar venda.")
    return db_venda

@router.get("/get", response_model=List[VendaRead])
def get_all_vendas_api(db: Session = Depends(get_db)):
    return venda_service.get_all_vendas(db)

@router.get("/get/{venda_id}", response_model=VendaRead)
def get_venda_by_id_api(venda_id: int, db: Session = Depends(get_db)):
    db_venda = venda_service.get_venda_by_id(db, venda_id)
    if not db_venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    return db_venda

@router.put("/update/{venda_id}", response_model=VendaRead)
def update_venda_api(venda_id: int, venda: VendaCreate, db: Session = Depends(get_db)):
    try:
        db_venda = venda_service.update_venda(db, venda_id, venda)
    except ValueError as e: # Captura a exceção de validação do Pydantic/Service
        raise HTTPException(status_code=400, detail=str(e))
    if not db_venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    return db_venda

@router.delete("/delete/{venda_id}", response_model=VendaRead)
def delete_venda_api(venda_id: int, db: Session = Depends(get_db)):
    db_venda = venda_service.delete_venda(db, venda_id)
    if not db_venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    return db_venda