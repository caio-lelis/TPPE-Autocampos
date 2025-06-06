from sqlalchemy.orm import Session
from src.models.moto import Moto
from src.models.concessionaria import Concessionaria
from src.schemas.moto_schema import MotoCreate

def criar_moto(db: Session, moto: MotoCreate):
    db_moto = Moto(**moto.dict())
    db.add(db_moto)
    db.commit()
    db.refresh(db_moto)
    return db_moto

def listar_motos(db: Session):
    return db.query(Moto).all()

def buscar_moto_por_id(db: Session, id_moto: int):
    return db.query(Moto).filter(Moto.id_moto == id_moto).first()

def get_moto_by_concessionaria(db: Session, id_concessionaria):
    motos = (
    db.query(Moto)
    .join(Concessionaria)
    .filter(Concessionaria.id_concessionaria == id_concessionaria)
    .all()
)
    return motos