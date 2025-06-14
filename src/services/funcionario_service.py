from sqlalchemy.orm import Session
from src.schemas.funcionario_schema import FuncionarioCreate
from src.models.funcionario import Funcionario as FuncionarioModel
from typing import List

class FuncionarioService:
    def create_funcionario(self, db: Session, funcionario: FuncionarioCreate) -> FuncionarioModel:
        db_funcionario = FuncionarioModel(
            usuario_id=funcionario.usuario_id,
            rendimento_mensal=funcionario.rendimento_mensal
        )
        db.add(db_funcionario)
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario

    def get_all_funcionarios(self, db: Session) -> List[FuncionarioModel]:
        return db.query(FuncionarioModel).all()

    def get_funcionario_by_id(self, db: Session, funcionario_id: int) -> FuncionarioModel:
        return db.query(FuncionarioModel).filter(FuncionarioModel.id == funcionario_id).first()

    def get_funcionario_by_usuario_id(self, db: Session, usuario_id: int) -> FuncionarioModel:
        return db.query(FuncionarioModel).filter(FuncionarioModel.usuario_id == usuario_id).first()

    def update_funcionario(self, db: Session, funcionario_id: int, funcionario: FuncionarioCreate) -> FuncionarioModel:
        db_funcionario = self.get_funcionario_by_id(db, funcionario_id)
        if not db_funcionario:
            return None
        db_funcionario.usuario_id = funcionario.usuario_id
        db_funcionario.rendimento_mensal = funcionario.rendimento_mensal
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario

    def delete_funcionario(self, db: Session, funcionario_id: int):
        db_funcionario = self.get_funcionario_by_id(db, funcionario_id)
        if not db_funcionario:
            return None
        db.delete(db_funcionario)
        db.commit()
        return db_funcionario

funcionario_service = FuncionarioService()