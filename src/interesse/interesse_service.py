from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError # Importar para lidar com erros de UNIQUE/CHECK
from src.interesse.interesse_schema import InteresseCreate
from src.interesse.interesse_model import Interesse as InteresseModel
from typing import List

class InteresseService:
    def create_interesse(self, db: Session, interesse: InteresseCreate) -> InteresseModel:
        try:
            db_interesse = InteresseModel(
                cliente_id=interesse.cliente_id,
                carro_id=interesse.carro_id,
                moto_id=interesse.moto_id,
                data_visita=interesse.data_visita,
                test_drive=interesse.test_drive
            )
            db.add(db_interesse)
            db.commit()
            db.refresh(db_interesse)
            return db_interesse
        except IntegrityError:
            db.rollback() # Reverte a transação em caso de erro de integridade (ex: duplicidade)
            raise ValueError("Interesse duplicado para este cliente e veículo.")


    def get_all_interesses(self, db: Session) -> List[InteresseModel]:
        return db.query(InteresseModel).all()

    def get_interesse_by_id(self, db: Session, interesse_id: int) -> InteresseModel:
        return db.query(InteresseModel).filter(InteresseModel.id == interesse_id).first()

    def update_interesse(self, db: Session, interesse_id: int, interesse: InteresseCreate) -> InteresseModel:
        db_interesse = self.get_interesse_by_id(db, interesse_id)
        if not db_interesse:
            return None
        
        # Validação da exclusividade
        if interesse.carro_id is not None and interesse.moto_id is not None:
            raise ValueError("Um interesse não pode ter carro_id e moto_id preenchidos simultaneamente.")
        if interesse.carro_id is None and interesse.moto_id is None:
            raise ValueError("Um interesse deve estar associado a um carro ou a uma moto.")

        db_interesse.cliente_id = interesse.cliente_id
        db_interesse.carro_id = interesse.carro_id
        db_interesse.moto_id = interesse.moto_id
        db_interesse.data_visita = interesse.data_visita
        db_interesse.test_drive = interesse.test_drive
        
        try:
            db.commit()
            db.refresh(db_interesse)
            return db_interesse
        except IntegrityError:
            db.rollback()
            raise ValueError("Atualização resultaria em interesse duplicado ou violação de restrição.")


    def delete_interesse(self, db: Session, interesse_id: int):
        db_interesse = self.get_interesse_by_id(db, interesse_id)
        if not db_interesse:
            return None
        db.delete(db_interesse)
        db.commit()
        return db_interesse

interesse_service = InteresseService()