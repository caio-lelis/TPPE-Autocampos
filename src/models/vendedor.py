# app/models/vendedor.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.models.pessoa import Pessoa
from src.models.base import Base

class Vendedor(Base):
    __tablename__ = 'vendedor'
    
    fk_Pessoa_id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True)
    salario = Column(Float, nullable=False)
    especialidade = Column(String(100))
    totalVendas = Column(Float, default=0.0)
    
    pessoa = relationship("Pessoa" , back_populates="vendedor")