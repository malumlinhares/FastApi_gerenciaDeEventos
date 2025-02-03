# backend/models/privilegio_vip.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class PrivilegioVip(Base):
    __tablename__ = "privilegios_vip"

    id = Column(Integer, primary_key=True)

    # Chave estrangeira para Participante (N:1)
    participante_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    # Chave estrangeira para Privilegio (N:1)
    privilegio_id = Column(Integer, ForeignKey("privilegios.id"), nullable=False)

    # Relacionamento com a tabela Privilegio
    privilegio = relationship("Privilegio", back_populates="privilegio_vip")
    # Relacionamento com a tabela Participante
    participante = relationship("Participante", back_populates="privilegio_vip")
