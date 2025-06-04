# src/routers/vendedor_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.services.vendedor_service import (
    create_vendedor,
    get_vendedor,
    get_vendedores,
    update_vendedor,
    delete_vendedor
)
from src.db.session import SessionLocal
from src.schemas.vendedor_schema import Vendedor, VendedorCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/vendedor",
             response_model=Vendedor,
             status_code=status.HTTP_201_CREATED,
             summary="Cria um novo vendedor")
def criar_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    """
    Cria um novo vendedor no sistema.
    
    - **pessoa_id**: ID da pessoa associada (obrigatório)
    - **salario**: Salário do vendedor (obrigatório)
    - **especialidade**: Área de especialização
    - **totalVendas**: Total de vendas acumuladas (default: 0.0)
    """
    try:
        return create_vendedor(db=db, vendedor=vendedor)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar vendedor: {str(e)}"
        )

@router.get("/{vendedor_id}",
            response_model=Vendedor,
            summary="Obtém um vendedor pelo ID")
def obter_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um vendedor específico pelo seu ID.
    """
    db_vendedor = get_vendedor(db, vendedor_id=vendedor_id)
    if db_vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado"
        )
    return db_vendedor

@router.get("/",
            response_model=List[Vendedor],
            summary="Lista todos os vendedores")
def listar_vendedores(db: Session = Depends(get_db)):
    """
    Retorna uma lista com todos os vendedores cadastrados no sistema.
    """
    return get_vendedores(db)

@router.put("/{vendedor_id}",
            response_model=Vendedor,
            summary="Atualiza um vendedor")
def atualizar_vendedor(
    vendedor_id: int, 
    vendedor: VendedorCreate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um vendedor existente.
    
    - Todos os campos são obrigatórios (serão substituídos)
    """
    db_vendedor = update_vendedor(
        db, 
        vendedor_id=vendedor_id, 
        vendedor=vendedor
    )
    if db_vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado"
        )
    return db_vendedor

@router.delete("/{vendedor_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove um vendedor")
def remover_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    """
    Remove permanentemente um vendedor do sistema.
    """
    success = delete_vendedor(db, vendedor_id=vendedor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado"
        )
