from sqlalchemy import Column, Integer, String, Boolean, Double, ForeignKey
from src.core.session import Base

class Carro(Base):
    __tablename__ = "carro"

    id_carro = Column(Integer, primary_key=True, autoincrement=True)
    num_portas = Column(Integer)
    vidros_eletricos = Column(Boolean)
    camera_re = Column(Boolean)
    airbags = Column(Boolean)
    marca = Column(String(100))
    modelo = Column(String(100))
    cor = Column(String(50))
    ano = Column(Integer)
    valor = Column(Double)
    tipo_combustivel = Column(String(50))

    fk_concessionaria_id_concessionaria = Column(Integer, ForeignKey("concessionaria.id_concessionaria", ondelete="SET NULL"))
    fk_comprador_id_comprador = Column(Integer, ForeignKey("comprador.id_comprador", ondelete="RESTRICT"), nullable=True)
    fk_vendedor_id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor", ondelete="CASCADE"), nullable=True)
