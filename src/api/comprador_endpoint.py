from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.comprador_schema import CompradorCreate, CompradorRead
from src.services import comprador_service


router = APIRouter(prefix="/compradores", tags=["Compradores"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CompradorRead)
def criar_comprador(comprador: CompradorCreate, db: Session = Depends(get_db)):
    return comprador_service.criar_comprador(db, comprador)

@router.get("/", response_model=list[CompradorRead])
def listar_compradores(db: Session = Depends(get_db)):
    return comprador_service.listar_compradores(db)

@router.get("/{id_comprador}/{id_pessoa}", response_model=CompradorRead)
def buscar_comprador(id_comprador: int, db: Session = Depends(get_db)):
    comprador = comprador_service.buscar_comprador_por_id(db, id_comprador)
    if not comprador:
        raise HTTPException(status_code=404, detail="Comprador não encontrado")
    return comprador
