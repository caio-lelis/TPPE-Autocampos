from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.caminhao_schema import CaminhaoCreate, CaminhaoRead
from src.services import caminhao_service

router = APIRouter(prefix="/caminhoes", tags=["Caminhões"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CaminhaoRead)
def create_caminhao(caminhao: CaminhaoCreate, db: Session = Depends(get_db)):
    return caminhao_service.create_caminhao(db, caminhao)

@router.get("/", response_model=list[CaminhaoRead])
def get_all_caminhoes(db: Session = Depends(get_db)):
    return caminhao_service.get_all_caminhoes(db)

@router.get("/{id_caminhao}", response_model=CaminhaoRead)
def buscar_caminhao(id_caminhao: int, db: Session = Depends(get_db)):
    caminhao = caminhao_service.get_caminhao_by_id(db, id_caminhao)
    if not caminhao:
        raise HTTPException(status_code=404, detail="Caminhão não encontrado")
    return caminhao
