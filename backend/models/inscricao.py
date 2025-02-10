from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from backend.config.database import Base  
from datetime import datetime

class Inscricao(Base):
    __tablename__ = 'inscricao'
    
    numero_inscricao = Column(Integer, primary_key=True, index=True)

    status = Column(String, index=True, default='Pendente', server_default='Pendente', nullable=False) 
    forma_pagamento = Column(String, index=True, nullable=False)
    valor = Column(Float, index=True, nullable=False)
    participante_id = Column(Integer, ForeignKey("participantes.id"),  nullable=False)
    #2 campos opcinais
    data_pagamento = Column(DateTime, nullable=True)  # Data do pagamento (opcional)
    observacao = Column(String, nullable=True)  
    participante = relationship("Participante", back_populates="inscricao")

