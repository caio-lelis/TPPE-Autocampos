# app/models/comprador.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .pessoa import Pessoa
from .base import Base

class Comprador(Base):
    __tablename__ = 'comprador'
    
    fk_Pessoa_id = Column(Integer, ForeignKey('Pessoa.id'), primary_key=True)
    email = Column(String(255), nullable=False)
    renda_mensal = Column(Float)
    profissao = Column(String(100))
    saldo_compra = Column(Float, default=0.0)
    
    pessoa = relationship("Pessoa")