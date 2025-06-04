# app/models/moto.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from .veiculo import Veiculo
from .base import Base

class Moto(Base):
    __tablename__ = 'moto'
    
    fk_Veiculo_id_veiculo = Column(Integer, ForeignKey('Veiculo.id_veiculo'), primary_key=True)
    cilindradas = Column(Integer)
    torque = Column(Float)
    peso = Column(Float)
    tipo_freio = Column(String(50))
    
    veiculo = relationship("Veiculo")