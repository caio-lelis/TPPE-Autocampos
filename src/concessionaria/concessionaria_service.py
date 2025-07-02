from sqlalchemy.orm import Session
from src.concessionaria.concessionaria import Concessionaria
from src.concessionaria.concessionaria_schema import ConcessionariaCreate

def create_concessionaria(db: Session, concessionaria: ConcessionariaCreate):
    db_concessionaria = Concessionaria(**concessionaria.dict())
    db.add(db_concessionaria)
    db.commit()
    db.refresh(db_concessionaria)
    return db_concessionaria

def get_all_concessionarias(db: Session):
    return db.query(Concessionaria).all()

def get_concessionaria_by_id(db: Session, id_concessionaria: int):
    return db.query(Concessionaria).filter(Concessionaria.id_concessionaria == id_concessionaria).first()
