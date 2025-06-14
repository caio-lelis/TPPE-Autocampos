from sqlalchemy import Column, Integer, String, Numeric, Boolean
from src.core.session import Base

class Carro(Base):
    __tablename__ = "carros"

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String(255), nullable=False)
    marca = Column(String(255), nullable=False)
    ano = Column(Integer, nullable=False)
    cor = Column(String(255))
    tipo_combustivel = Column(String(50))
    preco = Column(Numeric(10, 2), nullable=False)
    revisado = Column(Boolean, default=False)
    disponivel = Column(Boolean, default=True)
    tipo_direcao = Column(String(50))
    tracao = Column(String(10))
    consumo_cidade = Column(Numeric(4, 2))
    airbag = Column(Boolean, default=False)
    ar_condicionado = Column(Boolean, default=False)