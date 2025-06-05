from sqlalchemy import Column, Integer, String
from src.core.session import Base

class Concessionaria(Base):
    __tablename__ = "concessionaria"

    id_concessionaria = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255))
    endereco = Column(String(255))
    cnpj = Column(String(20))
    telefone = Column(String(20))
