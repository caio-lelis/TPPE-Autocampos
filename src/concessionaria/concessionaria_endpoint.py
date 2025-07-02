from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.concessionaria.concessionaria_schema import ConcessionariaCreate, ConcessionariaRead
from src.concessionaria import concessionaria_service


router = APIRouter(prefix="/concessionarias", tags=["Concessionárias"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=ConcessionariaRead)
def create_concessionaria(concessionaria: ConcessionariaCreate, db: Session = Depends(get_db)):
    return concessionaria_service.create_concessionaria(db, concessionaria)

@router.get("/get", response_model=list[ConcessionariaRead])
def get_all_concessionarias(db: Session = Depends(get_db)):
    return concessionaria_service.get_all_concessionarias(db)

@router.get("/get_by_id/{id_concessionaria}", response_model=ConcessionariaRead)
def buscar_concessionaria(id_concessionaria: int, db: Session = Depends(get_db)):
    db_concessionaria = concessionaria_service.get_concessionaria_by_id(db, id_concessionaria)
    if not db_concessionaria:
        raise HTTPException(status_code=404, detail="Concessionária não encontrada")
    return db_concessionaria
