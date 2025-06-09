from sqlalchemy.orm import Session
from src.models.caminhao import Caminhao
from src.schemas.caminhao_schema import CaminhaoCreate

def create_caminhao(db: Session, caminhao: CaminhaoCreate):
    db_caminhao = Caminhao(**caminhao.dict())
    db.add(db_caminhao)
    db.commit()
    db.refresh(db_caminhao)
    return db_caminhao

def get_all_caminhoes(db: Session):
    return db.query(Caminhao).all()

def get_caminhao_by_id(db: Session, id_caminhao: int):
    return db.query(Caminhao).filter(Caminhao.id_caminhao == id_caminhao).first()
