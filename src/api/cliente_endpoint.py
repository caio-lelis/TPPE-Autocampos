from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.cliente_schema import ClienteCreate, ClienteRead
from src.services.cliente_service import cliente_service
from typing import List

router = APIRouter(prefix="/clientes", tags=["Clientes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=ClienteRead)
def create_cliente_api(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = cliente_service.create_cliente(db, cliente)
    if not db_cliente:
        raise HTTPException(status_code=400, detail="Erro ao criar cliente.")
    return db_cliente

@router.get("/get", response_model=List[ClienteRead])
def get_all_clientes_api(db: Session = Depends(get_db)):
    return cliente_service.get_all_clientes(db)

@router.get("/get/{cliente_id}", response_model=ClienteRead)
def get_cliente_by_id_api(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = cliente_service.get_cliente_by_id(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return db_cliente

@router.put("/update/{cliente_id}", response_model=ClienteRead)
def update_cliente_api(cliente_id: int, cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = cliente_service.update_cliente(db, cliente_id, cliente)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return db_cliente

@router.delete("/delete/{cliente_id}", response_model=ClienteRead)
def delete_cliente_api(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = cliente_service.delete_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return db_cliente