# app/services/concessionaria_service.py
from typing import Optional
from sqlalchemy.orm import Session

from src.models.concessionaria import Concessionaria
from src.schemas.concessionaria_schema import ConcessionariaCreate

def create_concessionaria(db: Session, concessionaria: ConcessionariaCreate):
    db_concessionaria = Concessionaria(
        nome=concessionaria.nome,
        endereco=concessionaria.endereco,
        cnpj=concessionaria.cnpj,
        telefone=concessionaria.telefone
    )
    db.add(db_concessionaria)
    db.commit()
    db.refresh(db_concessionaria)
    return db_concessionaria

def get_concessionaria(db: Session, concessionaria_id: int):
    return db.query(Concessionaria).filter(Concessionaria.id_concessionaria == concessionaria_id).first()

def get_concessionarias(db: Session):
    return db.query(Concessionaria).all()

def delete_concessionaria(db: Session, concessionaria_id: int) -> bool:
    result = db.query(Concessionaria).filter(Concessionaria.id_concessionaria == concessionaria_id).delete()
    db.commit()
    return result > 0

def update_concessionaria(db: Session, concessionaria_id: int, concessionaria: ConcessionariaCreate):
    db.query(Concessionaria).filter(Concessionaria.id_concessionaria == concessionaria_id).update(concessionaria.dict())
    db.commit()
    return db.query(Concessionaria).filter(Concessionaria.id_concessionaria == concessionaria_id).first()
