from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from src.core.session import Base
from datetime import date

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    carro_id = Column(Integer, ForeignKey("carros.id", ondelete="RESTRICT"), unique=True)
    moto_id = Column(Integer, ForeignKey("motos.id", ondelete="RESTRICT"), unique=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="RESTRICT"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id", ondelete="RESTRICT"), nullable=False)
    data_venda = Column(Date, default=date.today, nullable=False)
    valor_final = Column(Numeric(10, 2), nullable=False)
    comissao_venda = Column(Numeric(10, 2))

    # A restrição CHECK é mais complexa de ser diretamente mapeada no SQLAlchemy ORM
    # mas o banco de dados cuidará disso. No ORM, a validação será feita no Schema/Service.
    __table_args__ = (
        CheckConstraint(
            '(carro_id IS NOT NULL AND moto_id IS NULL) OR (carro_id IS NULL AND moto_id IS NOT NULL)',
            name='chk_carro_moto_venda'
        ),
    )

    carro = relationship("Carro")
    moto = relationship("Moto")
    cliente = relationship("Cliente")
    funcionario = relationship("Funcionario")