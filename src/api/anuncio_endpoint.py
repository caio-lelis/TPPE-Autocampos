from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.moto_schema import MotoRead
from src.schemas.anuncio_schema import AnuncioCreate, AnuncioRead
from src.services.anuncio_service import anuncio_service
from src.schemas.carro_schema import CarroRead
from typing import List

router = APIRouter(prefix="/anuncios", tags=["Anúncios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=AnuncioRead)
def create_anuncio_api(anuncio: AnuncioCreate, db: Session = Depends(get_db)):
    try:
        db_anuncio = anuncio_service.create_anuncio(db, anuncio)
    except ValueError as e: # Captura a exceção de validação do Pydantic/Service
        raise HTTPException(status_code=400, detail=str(e))
    if not db_anuncio:
        raise HTTPException(status_code=400, detail="Erro ao criar anúncio.")
    return db_anuncio

@router.get("/get", response_model=List[AnuncioRead])
def get_all_anuncios_api(db: Session = Depends(get_db)):
    return anuncio_service.get_all_anuncios(db)

@router.get("/get/{anuncio_id}", response_model=AnuncioRead)
def get_anuncio_by_id_api(anuncio_id: int, db: Session = Depends(get_db)):
    db_anuncio = anuncio_service.get_anuncio_by_id(db, anuncio_id)
    if not db_anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado.")
    return db_anuncio

@router.put("/update/{anuncio_id}", response_model=AnuncioRead)
def update_anuncio_api(anuncio_id: int, anuncio: AnuncioCreate, db: Session = Depends(get_db)):
    try:
        db_anuncio = anuncio_service.update_anuncio(db, anuncio_id, anuncio)
    except ValueError as e: # Captura a exceção de validação do Pydantic/Service
        raise HTTPException(status_code=400, detail=str(e))
    if not db_anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado.")
    return db_anuncio

@router.delete("/delete/{anuncio_id}", response_model=AnuncioRead)
def delete_anuncio_api(anuncio_id: int, db: Session = Depends(get_db)):
    db_anuncio = anuncio_service.delete_anuncio(db, anuncio_id)
    if not db_anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado.")
    return db_anuncio

@router.get("/carros-anunciados/marca/{marca}", response_model=List[CarroRead])
def get_carros_anunciados_por_marca(marca: str, db: Session = Depends(get_db)):
    carros = anuncio_service.get_carros_anunciados_por_marca(db, marca)
    if not carros:
        raise HTTPException(status_code=404, detail="Nenhum carro anunciado encontrado para esta marca.")
    return carros


@router.get("/motos-anunciadas/marca/{marca}", response_model=List[MotoRead])
def get_motos_anunciadas_por_marca(marca: str, db: Session = Depends(get_db)):
    motos = anuncio_service.get_motos_anunciadas_por_marca(db, marca)
    if not motos:
        raise HTTPException(status_code=404, detail="Nenhuma moto anunciada encontrada para esta marca.")
    return motos
