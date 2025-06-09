from sqlalchemy.orm import Session
from src.models.comprador import Comprador
from src.schemas.comprador_schema import CompradorCreate

def create_comprador(db: Session, comprador: CompradorCreate):
    db_comprador = Comprador(**comprador.dict())
    db.add(db_comprador)
    db.commit()
    db.refresh(db_comprador)
    return db_comprador

def get_all_compradores(db: Session):
    return db.query(Comprador).all()

def get_comprador_by_id(db: Session, id_comprador: int):
    return db.query(Comprador).filter_by(id_comprador=id_comprador).first()
