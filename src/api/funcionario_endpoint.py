from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.schemas.funcionario_schema import FuncionarioCreate, FuncionarioRead
from src.services.funcionario_service import funcionario_service
from typing import List

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=FuncionarioRead)
def create_funcionario_api(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    db_funcionario = funcionario_service.create_funcionario(db, funcionario)
    if not db_funcionario:
        raise HTTPException(status_code=400, detail="Erro ao criar funcionário.")
    return db_funcionario

@router.get("/get", response_model=List[FuncionarioRead])
def get_all_funcionarios_api(db: Session = Depends(get_db)):
    return funcionario_service.get_all_funcionarios(db)

@router.get("/get/{funcionario_id}", response_model=FuncionarioRead)
def get_funcionario_by_id_api(funcionario_id: int, db: Session = Depends(get_db)):
    db_funcionario = funcionario_service.get_funcionario_by_id(db, funcionario_id)
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return db_funcionario

@router.put("/update/{funcionario_id}", response_model=FuncionarioRead)
def update_funcionario_api(funcionario_id: int, funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    db_funcionario = funcionario_service.update_funcionario(db, funcionario_id, funcionario)
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return db_funcionario

@router.delete("/delete/{funcionario_id}", response_model=FuncionarioRead)
def delete_funcionario_api(funcionario_id: int, db: Session = Depends(get_db)):
    db_funcionario = funcionario_service.delete_funcionario(db, funcionario_id)
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return db_funcionario