# backend/models/privilegio_vip.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class PrivilegioVip(Base):
    __tablename__ = "privilegios_vip"

    id = Column(Integer, primary_key=True)


    participante_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)

    privilegio_id = Column(Integer, ForeignKey("privilegios.id"), nullable=False)


    privilegio = relationship("Privilegio", back_populates="privilegio_vip")

    participante = relationship("Participante", back_populates="privilegio_vip", cascade="all, delete")
