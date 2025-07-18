from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.admin.admin_service import admin_service

router = APIRouter(prefix="/admin", tags=["Admin Home"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/metrics")
def get_admin_metrics(db: Session = Depends(get_db)):
    """
    Retorna métricas gerais do sistema para o painel do administrador
    """
    return admin_service.get_admin_home_metrics(db)

@router.get("/overview")
def get_admin_overview(db: Session = Depends(get_db)):
    """
    Retorna uma visão geral do negócio para o administrador
    """
    return admin_service.get_business_overview(db)
