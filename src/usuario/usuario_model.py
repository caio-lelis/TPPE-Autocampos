from sqlalchemy import Column, Integer, String
from src.core.session import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)