from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from backend.config.database import Base  

class Inscricao(Base):
    __tablename__ = 'inscricao'
    
    numero_inscricao = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    forma_pagamento = Column(String, index=True)
    valor = Column(Float, index=True)
    participante_id = Column(Integer, ForeignKey("participantes.id"),  nullable=False)

    participante = relationship("Participante", back_populates="inscricao", cascade="all, delete")

