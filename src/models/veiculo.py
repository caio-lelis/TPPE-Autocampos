# app/models/veiculo.py
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base

class TipoCombustivel(PyEnum):
    GASOLINA = "Gasolina"
    ALCOOL = "Álcool"
    DIESEL = "Diesel"
    FLEX = "Flex"
    ELETRICO = "Elétrico"
    HIBRIDO = "Híbrido"

class Veiculo(Base):
    __tablename__ = 'veiculo'
    
    id_veiculo = Column(Integer, primary_key=True, index=True)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    cor = Column(String(50))
    ano = Column(Integer)
    valor = Column(Float)
    tipo_combustivel = Column(Enum(TipoCombustivel))
    
    fk_Concessionaria_id_concessionaria = Column(Integer, ForeignKey('Concessionaria.id_concessionaria'))
    fk_Comprador_fk_Pessoa_id = Column(Integer, ForeignKey('Comprador.fk_Pessoa_id'))
    fk_Vendedor_fk_Pessoa_id = Column(Integer, ForeignKey('Vendedor.fk_Pessoa_id'))
    
    concessionaria = relationship("Concessionaria")
    comprador = relationship("Comprador")
    vendedor = relationship("Vendedor")