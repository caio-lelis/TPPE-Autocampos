from sqlalchemy.orm import Session
from src.schemas.carro_schema import CarroCreate
from src.models.carro import Carro as CarroModel
from typing import List

class CarroService:
    def create_carro(self, db: Session, carro: CarroCreate) -> CarroModel:
        db_carro = CarroModel(
            modelo=carro.modelo,
            marca=carro.marca,
            ano=carro.ano,
            cor=carro.cor,
            tipo_combustivel=carro.tipo_combustivel,
            preco=carro.preco,
            revisado=carro.revisado,
            disponivel=carro.disponivel,
            tipo_direcao=carro.tipo_direcao,
            tracao=carro.tracao,
            consumo_cidade=carro.consumo_cidade,
            airbag=carro.airbag,
            ar_condicionado=carro.ar_condicionado
        )
        db.add(db_carro)
        db.commit()
        db.refresh(db_carro)
        return db_carro

    def get_all_carros(self, db: Session) -> List[CarroModel]:
        return db.query(CarroModel).all()

    def get_carro_by_id(self, db: Session, carro_id: int) -> CarroModel:
        return db.query(CarroModel).filter(CarroModel.id == carro_id).first()

    def update_carro(self, db: Session, carro_id: int, carro: CarroCreate) -> CarroModel:
        db_carro = self.get_carro_by_id(db, carro_id)
        if not db_carro:
            return None
        db_carro.modelo = carro.modelo
        db_carro.marca = carro.marca
        db_carro.ano = carro.ano
        db_carro.cor = carro.cor
        db_carro.tipo_combustivel = carro.tipo_combustivel
        db_carro.preco = carro.preco
        db_carro.revisado = carro.revisado
        db_carro.disponivel = carro.disponivel
        db_carro.tipo_direcao = carro.tipo_direcao
        db_carro.tracao = carro.tracao
        db_carro.consumo_cidade = carro.consumo_cidade
        db_carro.airbag = carro.airbag
        db_carro.ar_condicionado = carro.ar_condicionado
        db.commit()
        db.refresh(db_carro)
        return db_carro

    def delete_carro(self, db: Session, carro_id: int):
        db_carro = self.get_carro_by_id(db, carro_id)
        if not db_carro:
            return None
        db.delete(db_carro)
        db.commit()
        return db_carro

carro_service = CarroService()