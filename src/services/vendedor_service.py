# src/services/vendedor_service.py
from typing import Optional
from sqlalchemy.orm import Session

from src.models.vendedor import Vendedor
from src.schemas.vendedor_schema import VendedorCreate

def create_vendedor(db: Session, vendedor: VendedorCreate):
    db_vendedor = Vendedor(
        fk_Pessoa_id=vendedor.pessoa_id,
        salario=vendedor.salario,
        especialidade=vendedor.especialidade,
        totalVendas=vendedor.totalVendas
    )
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def get_vendedor(db: Session, vendedor_id: int):
    return db.query(Vendedor).filter(Vendedor.fk_Pessoa_id == vendedor_id).first()

def get_vendedores(db: Session):
    return db.query(Vendedor).all()

def delete_vendedor(db: Session, vendedor_id: int) -> bool:
    result = db.query(Vendedor).filter(Vendedor.fk_Pessoa_id == vendedor_id).delete()
    db.commit()
    return result > 0

def update_vendedor(db: Session, vendedor_id: int, vendedor: VendedorCreate):
    db.query(Vendedor).filter(Vendedor.fk_Pessoa_id == vendedor_id).update({
        "salario": vendedor.salario,
        "especialidade": vendedor.especialidade,
        "totalVendas": vendedor.totalVendas
    })
    db.commit()
    return db.query(Vendedor).filter(Vendedor.fk_Pessoa_id == vendedor_id).first()