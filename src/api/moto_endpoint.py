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

@router.post("/", response_model=MotoRead)
def criar_moto(moto: MotoCreate, db: Session = Depends(get_db)):
    return moto_service.criar_moto(db, moto)

@router.get("/", response_model=list[MotoRead])
def listar_motos(db: Session = Depends(get_db)):
    return moto_service.listar_motos(db)

@router.get("/{id_moto}", response_model=MotoRead)
def buscar_moto(id_moto: int, db: Session = Depends(get_db)):
    moto = moto_service.buscar_moto_por_id(db, id_moto)
    if not moto:
        raise HTTPException(status_code=404, detail="Moto não encontrada")
    return moto
