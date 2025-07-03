from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from src.core.session import Base
from datetime import date

class Interesse(Base):
    __tablename__ = "interesses"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    carro_id = Column(Integer, ForeignKey("carros.id", ondelete="CASCADE"))
    moto_id = Column(Integer, ForeignKey("motos.id", ondelete="CASCADE"))
    data_visita = Column(Date)
    test_drive = Column(Boolean, default=False)

    __table_args__ = (
        # Garante que apenas um dos IDs de veículo seja preenchido
        CheckConstraint(
            '(carro_id IS NOT NULL AND moto_id IS NULL) OR (carro_id IS NULL AND moto_id IS NOT NULL)',
            name='chk_carro_moto_interesse'
        ),
        # Garante que um cliente não registre interesse duas vezes no mesmo carro ou moto
        UniqueConstraint('cliente_id', 'carro_id', 'moto_id', name='uq_cliente_veiculo_interesse'),
    )

    cliente = relationship("Cliente")
    carro = relationship("Carro")
    moto = relationship("Moto")