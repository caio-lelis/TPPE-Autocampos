# app/services/pessoa_service.py
from typing import Optional
from sqlalchemy.orm import Session

from src.models.pessoa import Pessoa
from src.schemas.pessoa_schema import PessoaCreate

def create_pessoa(db: Session, pessoa: PessoaCreate):
    db_pessoa = Pessoa(
        nome=pessoa.nome,
        cpf=pessoa.cpf,
        idade=pessoa.idade
    )
    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

def get_pessoa(db: Session, pessoa_id: int):
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

def get_pessoas(db: Session):
    return db.query(Pessoa).all()

def delete_pessoa(db: Session, pessoa_id: int) -> bool:
    result = db.query(Pessoa).filter(Pessoa.id == pessoa_id).delete()
    db.commit()
    return result > 0

def update_pessoa(db: Session, pessoa_id: int, pessoa: PessoaCreate):
    db.query(Pessoa).filter(Pessoa.id == pessoa_id).update(pessoa.dict())
    db.commit()
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
