from sqlalchemy.orm import Session
from src.usuario.usuario_schema import UsuarioCreate
from src.usuario.usuario_model import Usuario as UserModel
from typing import List

class UsuarioService:
    def create_usuario(self, db: Session, usuario: UsuarioCreate) -> UserModel:
        db_usuario = UserModel(
            nome=usuario.nome,
            cpf=usuario.cpf,
            email=usuario.email,
            senha=usuario.senha # Lembre-se de hashear a senha em um projeto real
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def get_all_usuarios(self, db: Session) -> List[UserModel]:
        return db.query(UserModel).all()

    def get_usuario_by_id(self, db: Session, usuario_id: int) -> UserModel:
        return db.query(UserModel).filter(UserModel.id == usuario_id).first()

    def update_usuario(self, db: Session, usuario_id: int, usuario: UsuarioCreate) -> UserModel:
        db_usuario = self.get_usuario_by_id(db, usuario_id)
        if not db_usuario:
            return None
        db_usuario.nome = usuario.nome
        db_usuario.cpf = usuario.cpf
        db_usuario.email = usuario.email
        db_usuario.senha = usuario.senha # Lembre-se de hashear a senha em um projeto real
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def delete_usuario(self, db: Session, usuario_id: int):
        db_usuario = self.get_usuario_by_id(db, usuario_id)
        if not db_usuario:
            return None
        db.delete(db_usuario)
        db.commit()
        return db_usuario

usuario_service = UsuarioService()