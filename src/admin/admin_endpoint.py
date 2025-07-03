from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.admin.admin_schema import AdminCreate, AdminRead
from src.admin.admin_service import admin_service
from typing import List

router = APIRouter(prefix="/admins", tags=["Administradores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=AdminRead)
def create_admin_api(admin: AdminCreate, db: Session = Depends(get_db)):
    db_admin = admin_service.create_admin(db, admin)
    if not db_admin:
        raise HTTPException(status_code=400, detail="Erro ao criar administrador.")
    return db_admin

@router.get("/get", response_model=List[AdminRead])
def get_all_admins_api(db: Session = Depends(get_db)):
    return admin_service.get_all_admins(db)

@router.get("/get/{admin_id}", response_model=AdminRead)
def get_admin_by_id_api(admin_id: int, db: Session = Depends(get_db)):
    db_admin = admin_service.get_admin_by_id(db, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Administrador não encontrado.")
    return db_admin

@router.put("/update/{admin_id}", response_model=AdminRead)
def update_admin_api(admin_id: int, admin: AdminCreate, db: Session = Depends(get_db)):
    db_admin = admin_service.update_admin(db, admin_id, admin)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Administrador não encontrado.")
    return db_admin

@router.delete("/delete/{admin_id}", response_model=AdminRead)
def delete_admin_api(admin_id: int, db: Session = Depends(get_db)):
    db_admin = admin_service.delete_admin(db, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Administrador não encontrado.")
    return db_admin