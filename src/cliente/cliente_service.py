from sqlalchemy.orm import Session
from src.cliente.cliente_schema import ClienteCreate
from src.cliente.cliente import Cliente as ClienteModel
from typing import List

class ClienteService:
    def create_cliente(self, db: Session, cliente: ClienteCreate) -> ClienteModel:
        db_cliente = ClienteModel(
            nome=cliente.nome,
            cpf=cliente.cpf,
            email=cliente.email,
            telefone=cliente.telefone,
            endereco=cliente.endereco
        )
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    def get_all_clientes(self, db: Session) -> List[ClienteModel]:
        return db.query(ClienteModel).all()

    def get_cliente_by_id(self, db: Session, cliente_id: int) -> ClienteModel:
        return db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()

    def update_cliente(self, db: Session, cliente_id: int, cliente: ClienteCreate) -> ClienteModel:
        db_cliente = self.get_cliente_by_id(db, cliente_id)
        if not db_cliente:
            return None
        db_cliente.nome = cliente.nome
        db_cliente.cpf = cliente.cpf
        db_cliente.email = cliente.email
        db_cliente.telefone = cliente.telefone
        db_cliente.endereco = cliente.endereco
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    def delete_cliente(self, db: Session, cliente_id: int):
        db_cliente = self.get_cliente_by_id(db, cliente_id)
        if not db_cliente:
            return None
        db.delete(db_cliente)
        db.commit()
        return db_cliente

cliente_service = ClienteService()