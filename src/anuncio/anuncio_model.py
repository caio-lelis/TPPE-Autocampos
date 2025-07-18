from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from src.core.session import Base
from datetime import date

class Anuncio(Base):
    __tablename__ = "anuncios"

    id = Column(Integer, primary_key=True, index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)
    carro_id = Column(Integer, ForeignKey("carros.id", ondelete="CASCADE"), unique=True)
    moto_id = Column(Integer, ForeignKey("motos.id", ondelete="CASCADE"), unique=True)
    data_publicacao = Column(Date, default=date.today, nullable=False)
    imagem1_url = Column(String(255))
    imagem2_url = Column(String(255))
    imagem3_url = Column(String(255))

    # A restrição CHECK é mais complexa de ser diretamente mapeada no SQLAlchemy ORM
    # mas o banco de dados cuidará disso. No ORM, a validação será feita no Schema/Service.
    __table_args__ = (
        CheckConstraint(
            '(carro_id IS NOT NULL AND moto_id IS NULL) OR (carro_id IS NULL AND moto_id IS NOT NULL)',
            name='chk_carro_moto_anuncio'
        ),
    )

    funcionario = relationship("Funcionario")
    carro = relationship("Carro")
    moto = relationship("Moto")