from sqlalchemy.orm import Session
from src.models.vendedor import Vendedor
from src.schemas.vendedor_schema import VendedorCreate

def create_vendedor(db: Session, vendedor: VendedorCreate):
    db_vendedor = Vendedor(**vendedor.dict())
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def get_all_vendedores(db: Session):
    return db.query(Vendedor).all()

def get_vendedor_by_id(db: Session, id_vendedor: int):
    return db.query(Vendedor).filter_by(id_vendedor=id_vendedor).first()
