# app/models/comprador.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.models.pessoa import Pessoa
from src.models.base import Base

class Comprador(Base):
    __tablename__ = 'comprador'
    
    fk_Pessoa_id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True)
    email = Column(String(255), nullable=False)
    renda_mensal = Column(Float)
    profissao = Column(String(100))
    saldo_compra = Column(Float, default=0.0)
    
    pessoa = relationship("Pessoa", back_populates="comprador")

    