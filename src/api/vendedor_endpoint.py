from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.vendedor_schema import VendedorCreate, VendedorRead
from src.services import vendedor_service


router = APIRouter(prefix="/vendedores", tags=["Vendedores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=VendedorRead)
def create_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    return vendedor_service.create_vendedor(db, vendedor)

@router.get("/", response_model=list[VendedorRead])
def get_all_vendedores(db: Session = Depends(get_db)):
    return vendedor_service.get_all_vendedores(db)

@router.get("/{id_vendedor}/{id_pessoa}", response_model=VendedorRead)
def buscar_vendedor(id_vendedor: int, db: Session = Depends(get_db)):
    vendedor = vendedor_service.get_vendedor_by_id(db, id_vendedor)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return vendedor
