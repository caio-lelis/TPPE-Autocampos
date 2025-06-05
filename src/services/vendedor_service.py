from sqlalchemy.orm import Session
from src.models.vendedor import Vendedor
from src.schemas.vendedor_schema import VendedorCreate

def criar_vendedor(db: Session, vendedor: VendedorCreate):
    db_vendedor = Vendedor(**vendedor.dict())
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def listar_vendedores(db: Session):
    return db.query(Vendedor).all()

def buscar_vendedor_por_id(db: Session, id_vendedor: int):
    return db.query(Vendedor).filter_by(id_vendedor=id_vendedor).first()
