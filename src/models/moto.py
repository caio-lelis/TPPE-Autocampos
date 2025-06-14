from sqlalchemy import Column, Integer, String, Numeric, Boolean
from src.core.session import Base

class Moto(Base):
    __tablename__ = "motos"

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String(255), nullable=False)
    marca = Column(String(255), nullable=False)
    ano = Column(Integer, nullable=False)
    cor = Column(String(255))
    tipo_combustivel = Column(String(50))
    preco = Column(Numeric(10, 2), nullable=False)
    revisado = Column(Boolean, default=False)
    disponivel = Column(Boolean, default=True)
    freio_dianteiro = Column(String(50))
    freio_traseiro = Column(String(50))
    estilo = Column(String(50))
    cilindradas = Column(Integer)
    velocidade_max = Column(Integer)