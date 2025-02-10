from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from backend.config.database import Base
from datetime import datetime


class Certificado(Base):
    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True)

    # 3 campos obrigatorios:
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    participante_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    autenticador_id = Column(Integer, ForeignKey("autenticadores.id"), nullable=True)  
    
    # 2 campos opcionais
    data_emissao = Column(DateTime, nullable=True, default=datetime.utcnow)  # Data de emissão opcional
    codigo_verificacao = Column(String, unique=True, nullable=True)  # Código único para validação


    # Relacionamentos
    evento = relationship("Evento", back_populates="certificado")
    participante = relationship("Participante", back_populates="certificado")
    autenticador = relationship("Autenticador", back_populates="certificado", uselist=False)  # Cada certificado pode ter um autenticador
