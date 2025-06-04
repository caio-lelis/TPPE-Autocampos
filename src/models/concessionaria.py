# app/models/concessionaria.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Concessionaria(Base):
    __tablename__ = 'concessionaria'
    
    id_concessionaria = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255))
    endereco = Column(String(255))
    cnpj = Column(String(18), unique=True)
    telefone = Column(String(20))