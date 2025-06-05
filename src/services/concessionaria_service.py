from sqlalchemy.orm import Session
from src.models.concessionaria import Concessionaria
from src.schemas.concessionaria_schema import ConcessionariaCreate

def criar_concessionaria(db: Session, concessionaria: ConcessionariaCreate):
    db_concessionaria = Concessionaria(**concessionaria.dict())
    db.add(db_concessionaria)
    db.commit()
    db.refresh(db_concessionaria)
    return db_concessionaria

def listar_concessionarias(db: Session):
    return db.query(Concessionaria).all()

def buscar_concessionaria_por_id(db: Session, id_concessionaria: int):
    return db.query(Concessionaria).filter(Concessionaria.id_concessionaria == id_concessionaria).first()
