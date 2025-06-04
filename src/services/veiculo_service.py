# app/services/veiculo_service.py
from typing import Optional
from sqlalchemy.orm import Session

from src.models.veiculo import Veiculo
from src.schemas.veiculo_schema import VeiculoCreate

def create_veiculo(db: Session, veiculo: VeiculoCreate):
    db_veiculo = Veiculo(
        marca=veiculo.marca,
        modelo=veiculo.modelo,
        cor=veiculo.cor,
        ano=veiculo.ano,
        valor=veiculo.valor,
        tipo_combustivel=veiculo.tipo_combustivel,
        fk_Concessionaria_id_concessionaria=veiculo.concessionaria_id,
        fk_Comprador_fk_Pessoa_id=veiculo.comprador_id,
        fk_Vendedor_fk_Pessoa_id=veiculo.vendedor_id
    )
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo

def get_veiculo(db: Session, veiculo_id: int):
    return db.query(Veiculo).filter(Veiculo.id_veiculo == veiculo_id).first()

def get_veiculos(db: Session):
    return db.query(Veiculo).all()

def delete_veiculo(db: Session, veiculo_id: int) -> bool:
    result = db.query(Veiculo).filter(Veiculo.id_veiculo == veiculo_id).delete()
    db.commit()
    return result > 0

def update_veiculo(db: Session, veiculo_id: int, veiculo: VeiculoCreate):
    db.query(Veiculo).filter(Veiculo.id_veiculo == veiculo_id).update(veiculo.dict())
    db.commit()
    return db.query(Veiculo).filter(Veiculo.id_veiculo == veiculo_id).first()