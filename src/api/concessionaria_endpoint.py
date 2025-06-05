from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.concessionaria_schema import ConcessionariaCreate, ConcessionariaRead
from src.services import concessionaria_service


router = APIRouter(prefix="/concessionarias", tags=["Concessionárias"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ConcessionariaRead)
def criar_concessionaria(concessionaria: ConcessionariaCreate, db: Session = Depends(get_db)):
    return concessionaria_service.criar_concessionaria(db, concessionaria)

@router.get("/", response_model=list[ConcessionariaRead])
def listar_concessionarias(db: Session = Depends(get_db)):
    return concessionaria_service.listar_concessionarias(db)

@router.get("/{id_concessionaria}", response_model=ConcessionariaRead)
def buscar_concessionaria(id_concessionaria: int, db: Session = Depends(get_db)):
    db_concessionaria = concessionaria_service.buscar_concessionaria_por_id(db, id_concessionaria)
    if not db_concessionaria:
        raise HTTPException(status_code=404, detail="Concessionária não encontrada")
    return db_concessionaria
