from sqlalchemy import Column, Integer, String, Double, PrimaryKeyConstraint
from src.core.session import Base

class Vendedor(Base):
    __tablename__ = "vendedor"

    id_vendedor = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255))
    cpf = Column(String(14))
    idade = Column(Integer)
    salario = Column(Double)
    especialidade = Column(String(100))
    total_vendas = Column(Double)
