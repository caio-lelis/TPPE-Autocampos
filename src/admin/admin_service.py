from sqlalchemy.orm import Session
from src.admin.admin_schema import AdminCreate
from src.admin.admin_model import Admin as AdminModel
from typing import List

class AdminService:
    def create_admin(self, db: Session, admin: AdminCreate) -> AdminModel:
        db_admin = AdminModel(
            usuario_id=admin.usuario_id,
            is_admin=admin.is_admin
        )
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        return db_admin

    def get_all_admins(self, db: Session) -> List[AdminModel]:
        return db.query(AdminModel).all()

    def get_admin_by_id(self, db: Session, admin_id: int) -> AdminModel:
        return db.query(AdminModel).filter(AdminModel.id == admin_id).first()

    def get_admin_by_usuario_id(self, db: Session, usuario_id: int) -> AdminModel:
        return db.query(AdminModel).filter(AdminModel.usuario_id == usuario_id).first()

    def update_admin(self, db: Session, admin_id: int, admin: AdminCreate) -> AdminModel:
        db_admin = self.get_admin_by_id(db, admin_id)
        if not db_admin:
            return None
        db_admin.usuario_id = admin.usuario_id
        db_admin.is_admin = admin.is_admin
        db.commit()
        db.refresh(db_admin)
        return db_admin

    def delete_admin(self, db: Session, admin_id: int):
        db_admin = self.get_admin_by_id(db, admin_id)
        if not db_admin:
            return None
        db.delete(db_admin)
        db.commit()
        return db_admin

admin_service = AdminService()