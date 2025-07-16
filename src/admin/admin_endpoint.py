from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.admin.admin_schema import AdminCreate, AdminRead
from src.admin.admin_service import admin_service
from typing import List
from pydantic import BaseModel
from src.usuario.usuario_service import usuario_service
from src.admin.admin_model import Admin

router = APIRouter(prefix="/admins", tags=["Administradores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=AdminRead)
def create_admin_api(admin: AdminCreate, db: Session = Depends(get_db)):
    # Garante que is_admin seja sempre true
    admin.is_admin = True
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

class AdminLogin(BaseModel):
    email: str
    senha: str

@router.post("/login")
def login_admin_api(login: AdminLogin, db: Session = Depends(get_db)):
    # Autentica usuário
    usuario = usuario_service.authenticate_usuario(db, login.email, login.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos.")
    # Verifica se é admin
    admin = db.query(Admin).filter(Admin.usuario_id == usuario.id, Admin.is_admin == True).first()
    if not admin:
        raise HTTPException(status_code=403, detail="Não autorizado como administrador.")
    # Retorna dados do admin
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": "admin"
    }

# Endpoint de dashboard para administradores: métricas e gráfico
@router.get("/dashboard")
def get_admin_dashboard(db: Session = Depends(get_db)):
    stats, img_b64 = admin_service.get_dashboard_stats(db)
    return {"metricas": stats, "grafico": f"data:image/png;base64,{img_b64}"}