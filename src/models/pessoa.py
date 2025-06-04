# app/models/pessoa.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoa'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    idade = Column(Integer)
    
    vendedor = relationship("Vendedor", back_populates="pessoa", uselist=False)
    comprador = relationship("Comprador", back_populates="pessoa", uselist=False)