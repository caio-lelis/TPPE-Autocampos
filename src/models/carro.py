# app/models/carro.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .veiculo import Veiculo
from .base import Base

class Carro(Base):
    __tablename__ = 'carro'
    
    fk_Veiculo_id_veiculo = Column(Integer, ForeignKey('Veiculo.id_veiculo'), primary_key=True)
    num_portas = Column(Integer)
    vidros_eletricos = Column(Boolean, default=False)
    camera_re = Column(Boolean, default=False)
    airbags = Column(Boolean, default=False)
    
    veiculo = relationship("Veiculo")
