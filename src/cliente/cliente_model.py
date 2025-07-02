from sqlalchemy import Column, Integer, String
from src.core.session import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    email = Column(String(255), unique=True)
    telefone = Column(String(20))
    endereco = Column(String(255))