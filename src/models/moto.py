from sqlalchemy import Column, Integer, String, Double, ForeignKey
from src.core.session import Base

class Moto(Base):
    __tablename__ = "moto"

    id_moto = Column(Integer, primary_key=True, autoincrement=True)
    cilindradas = Column(Integer)
    torque = Column(Double)
    peso = Column(Double)
    tipo_freio = Column(String(50))
    marca = Column(String(100))
    modelo = Column(String(100))
    cor = Column(String(50))
    ano = Column(Integer)
    valor = Column(Double)
    tipo_combustivel = Column(String(50))

    fk_concessionaria_id_concessionaria = Column(Integer, ForeignKey("concessionaria.id_concessionaria", ondelete="SET NULL"))
    fk_comprador_id_comprador = Column(Integer, ForeignKey("comprador.id_comprador", ondelete="RESTRICT"), nullable=True)
    fk_vendedor_id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor", ondelete="CASCADE"), nullable=True)
