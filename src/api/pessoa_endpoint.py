# src/routers/pessoa_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.services.pessoa_service import (
    create_pessoa,
    get_pessoa,
    get_pessoas,
    update_pessoa,
    delete_pessoa
)

from src.db.session import SessionLocal

# Importa o schema Pydantic com alias para evitar confusão
from src.schemas.pessoa_schema import Pessoa as PessoaSchema, PessoaCreate
# Importa o modelo SQLAlchemy
from src.models.pessoa import Pessoa as PessoaModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pessoa",
             response_model=PessoaSchema,  # <- schema Pydantic
             status_code=status.HTTP_201_CREATED,
             summary="Cadastra uma nova pessoa")
def cadastrar_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db)):
    try:
        if db.query(PessoaModel).filter(PessoaModel.cpf == pessoa.cpf).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado"
            )
        return create_pessoa(db=db, pessoa=pessoa)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cadastrar pessoa: {str(e)}"
        )


@router.get("/{pessoa_id}",
            response_model=PessoaSchema,
            summary="Obtém uma pessoa pelo ID")
def obter_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de uma pessoa específica pelo seu ID.
    """
    db_pessoa = get_pessoa(db, pessoa_id=pessoa_id)
    if db_pessoa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada"
        )
    return db_pessoa

@router.get("/",
            response_model=List[PessoaSchema],
            summary="Lista todas as pessoas")
def listar_pessoas(db: Session = Depends(get_db)):
    """
    Retorna uma lista com todas as pessoas cadastradas no sistema.
    """
    return get_pessoas(db)

@router.put("/{pessoa_id}",
            response_model=PessoaSchema,
            summary="Atualiza uma pessoa")
def atualizar_pessoa(
    pessoa_id: int, 
    pessoa: PessoaCreate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de uma pessoa existente.
    
    - Todos os campos são obrigatórios (serão substituídos)
    - Não é possível alterar o CPF
    """
    db_pessoa = update_pessoa(
        db, 
        pessoa_id=pessoa_id, 
        pessoa=pessoa
    )
    if db_pessoa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada"
        )
    return db_pessoa

@router.delete("/{pessoa_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove uma pessoa")
def remover_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    """
    Remove permanentemente uma pessoa do sistema.
    
    Atenção: Esta operação também removerá registros associados (vendedor/comprador).
    """
    success = delete_pessoa(db, pessoa_id=pessoa_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada"
        )