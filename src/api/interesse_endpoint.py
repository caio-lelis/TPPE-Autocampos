from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.interesse_schema import InteresseCreate, InteresseRead
from src.services.interesse_service import interesse_service
from typing import List

router = APIRouter(prefix="/interesses", tags=["Interesses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=InteresseRead, status_code=status.HTTP_201_CREATED)
def create_interesse_api(interesse: InteresseCreate, db: Session = Depends(get_db)):
    try:
        db_interesse = interesse_service.create_interesse(db, interesse)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_interesse

@router.get("/get", response_model=List[InteresseRead])
def get_all_interesses_api(db: Session = Depends(get_db)):
    return interesse_service.get_all_interesses(db)

@router.get("/get/{interesse_id}", response_model=InteresseRead)
def get_interesse_by_id_api(interesse_id: int, db: Session = Depends(get_db)):
    db_interesse = interesse_service.get_interesse_by_id(db, interesse_id)
    if not db_interesse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interesse não encontrado.")
    return db_interesse

@router.put("/update/{interesse_id}", response_model=InteresseRead)
def update_interesse_api(interesse_id: int, interesse: InteresseCreate, db: Session = Depends(get_db)):
    try:
        db_interesse = interesse_service.update_interesse(db, interesse_id, interesse)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not db_interesse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interesse não encontrado.")
    return db_interesse

@router.delete("/delete/{interesse_id}", response_model=InteresseRead)
def delete_interesse_api(interesse_id: int, db: Session = Depends(get_db)):
    db_interesse = interesse_service.delete_interesse(db, interesse_id)
    if not db_interesse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interesse não encontrado.")
    return db_interesse