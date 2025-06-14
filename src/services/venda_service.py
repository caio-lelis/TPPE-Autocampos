from sqlalchemy.orm import Session
from src.schemas.venda_schema import VendaCreate
from src.models.venda import Venda as VendaModel
from typing import List

class VendaService:
    def create_venda(self, db: Session, venda: VendaCreate) -> VendaModel:
        db_venda = VendaModel(
            carro_id=venda.carro_id,
            moto_id=venda.moto_id,
            cliente_id=venda.cliente_id,
            funcionario_id=venda.funcionario_id,
            data_venda=venda.data_venda,
            valor_final=venda.valor_final,
            comissao_venda=venda.comissao_venda
        )
        db.add(db_venda)
        db.commit()
        db.refresh(db_venda)
        return db_venda

    def get_all_vendas(self, db: Session) -> List[VendaModel]:
        return db.query(VendaModel).all()

    def get_venda_by_id(self, db: Session, venda_id: int) -> VendaModel:
        return db.query(VendaModel).filter(VendaModel.id == venda_id).first()

    def update_venda(self, db: Session, venda_id: int, venda: VendaCreate) -> VendaModel:
        db_venda = self.get_venda_by_id(db, venda_id)
        if not db_venda:
            return None
        
        # Validação da exclusividade também no update
        if venda.carro_id is not None and venda.moto_id is not None:
            raise ValueError("Uma venda não pode ter carro_id e moto_id preenchidos simultaneamente.")
        if venda.carro_id is None and venda.moto_id is None:
            raise ValueError("Uma venda deve estar associada a um carro ou a uma moto.")

        db_venda.carro_id = venda.carro_id
        db_venda.moto_id = venda.moto_id
        db_venda.cliente_id = venda.cliente_id
        db_venda.funcionario_id = venda.funcionario_id
        db_venda.data_venda = venda.data_venda
        db_venda.valor_final = venda.valor_final
        db_venda.comissao_venda = venda.comissao_venda
        db.commit()
        db.refresh(db_venda)
        return db_venda

    def delete_venda(self, db: Session, venda_id: int):
        db_venda = self.get_venda_by_id(db, venda_id)
        if not db_venda:
            return None
        db.delete(db_venda)
        db.commit()
        return db_venda

venda_service = VendaService()