from sqlalchemy import Column, Integer, String, Double, PrimaryKeyConstraint
from src.core.session import Base

class Comprador(Base):
    __tablename__ = "comprador"

    
    id_comprador = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255))
    cpf = Column(String(14))
    idade = Column(Integer)
    email = Column(String(255))
    renda_mensal = Column(Double)
    profissao = Column(String(100))
    saldo_compra = Column(Double)

