from sqlalchemy.orm import Session
from src.moto.moto_schema import MotoCreate
from src.moto.moto_model import Moto as MotoModel
from typing import List

class MotoService:
    def create_moto(self, db: Session, moto: MotoCreate) -> MotoModel:
        db_moto = MotoModel(
            modelo=moto.modelo,
            marca=moto.marca,
            ano=moto.ano,
            cor=moto.cor,
            tipo_combustivel=moto.tipo_combustivel,
            preco=moto.preco,
            revisado=moto.revisado,
            disponivel=moto.disponivel,
            freio_dianteiro=moto.freio_dianteiro,
            freio_traseiro=moto.freio_traseiro,
            estilo=moto.estilo,
            cilindradas=moto.cilindradas,
            velocidade_max=moto.velocidade_max
        )
        db.add(db_moto)
        db.commit()
        db.refresh(db_moto)
        return db_moto

    def get_all_motos(self, db: Session) -> List[MotoModel]:
        return db.query(MotoModel).all()

    def get_moto_by_id(self, db: Session, moto_id: int) -> MotoModel:
        return db.query(MotoModel).filter(MotoModel.id == moto_id).first()

    def update_moto(self, db: Session, moto_id: int, moto: MotoCreate) -> MotoModel:
        db_moto = self.get_moto_by_id(db, moto_id)
        if not db_moto:
            return None
        db_moto.modelo = moto.modelo
        db_moto.marca = moto.marca
        db_moto.ano = moto.ano
        db_moto.cor = moto.cor
        db_moto.tipo_combustivel = moto.tipo_combustivel
        db_moto.preco = moto.preco
        db_moto.revisado = moto.revisado
        db_moto.disponivel = moto.disponivel
        db_moto.freio_dianteiro = moto.freio_dianteiro
        db_moto.freio_traseiro = moto.freio_traseiro
        db_moto.estilo = moto.estilo
        db_moto.cilindradas = moto.cilindradas
        db_moto.velocidade_max = moto.velocidade_max
        db.commit()
        db.refresh(db_moto)
        return db_moto

    def delete_moto(self, db: Session, moto_id: int):
        db_moto = self.get_moto_by_id(db, moto_id)
        if not db_moto:
            return None
        db.delete(db_moto)
        db.commit()
        return db_moto

moto_service = MotoService()