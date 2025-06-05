from sqlalchemy import Column, Integer, String, Float, Double, ForeignKey
from src.core.session import Base

class Caminhao(Base):
    __tablename__ = "caminhao"

    id_caminhao = Column(Integer, primary_key=True, autoincrement=True)
    carga = Column(Float)
    tamanho = Column(Float)
    tipo_carroceria = Column(String(100))
    num_eixos = Column(Integer)
    marca = Column(String(100))
    modelo = Column(String(100))
    cor = Column(String(50))
    ano = Column(Integer)
    valor = Column(Double)
    tipo_combustivel = Column(String(50))

    fk_concessionaria_id_concessionaria = Column(Integer, ForeignKey("concessionaria.id_concessionaria", ondelete="SET NULL"))
    fk_comprador_id_comprador = Column(Integer, ForeignKey("comprador.id_comprador", ondelete="RESTRICT"), nullable=True)
    fk_vendedor_id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor", ondelete="CASCADE"), nullable=True)
