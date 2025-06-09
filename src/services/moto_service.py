from sqlalchemy.orm import Session
from src.models.moto import Moto
from src.models.concessionaria import Concessionaria
from src.schemas.moto_schema import MotoCreate

def create_moto(db: Session, moto: MotoCreate):
    """
    criação de um objeto moto
    """
    db_moto = Moto(**moto.dict())
    db.add(db_moto)
    db.commit()
    db.refresh(db_moto)
    return db_moto

def get_all_motos(db: Session):
    """
    Retorna todos os objetos motos existentes
    """
    return db.query(Moto).all()

def get_moto_by_id(db: Session, id_moto: int):
    """
    Retorna uma moto pelo Id correspondente
    """
    return db.query(Moto).filter(Moto.id_moto == id_moto).first()

def get_moto_by_concessionaria(db: Session, id_concessionaria):
    """
    Retorna todos os objetos motos de uma determinada concessionaria
    """
    motos = (
    db.query(Moto)
    .join(Concessionaria)
    .filter(Concessionaria.id_concessionaria == id_concessionaria)
    .all()
)
    return motos