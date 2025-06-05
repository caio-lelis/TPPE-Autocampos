from sqlalchemy.orm import Session
from src.models.comprador import Comprador
from src.schemas.comprador_schema import CompradorCreate

def criar_comprador(db: Session, comprador: CompradorCreate):
    db_comprador = Comprador(**comprador.dict())
    db.add(db_comprador)
    db.commit()
    db.refresh(db_comprador)
    return db_comprador

def listar_compradores(db: Session):
    return db.query(Comprador).all()

def buscar_comprador_por_id(db: Session, id_comprador: int):
    return db.query(Comprador).filter_by(id_comprador=id_comprador).first()
