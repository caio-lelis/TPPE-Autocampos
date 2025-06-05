from sqlalchemy.orm import Session
from src.models.carro import Carro
from src.schemas.carro_schema import CarroCreate

def criar_carro(db: Session, carro: CarroCreate):
    db_carro = Carro(**carro.dict())
    db.add(db_carro)
    db.commit()
    db.refresh(db_carro)
    return db_carro

def listar_carros(db: Session):
    return db.query(Carro).all()

def buscar_carro_por_id(db: Session, id_carro: int):
    return db.query(Carro).filter(Carro.id_carro == id_carro).first()
