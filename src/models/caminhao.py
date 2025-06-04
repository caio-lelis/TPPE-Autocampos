# app/models/caminhao.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from .veiculo import Veiculo
from .base import Base

class Caminhao(Base):
    __tablename__ = 'caminhao'
    
    fk_Veiculo_id_veiculo = Column(Integer, ForeignKey('Veiculo.id_veiculo'), primary_key=True)
    carga = Column(Float)
    tamanho = Column(Float)
    tipo_carroceria = Column(String(50))
    num_eixos = Column(Integer)
    
    veiculo = relationship("Veiculo")