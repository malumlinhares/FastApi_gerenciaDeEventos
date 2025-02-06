# backend/models/evento.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Evento(Base):
    __tablename__ = 'eventos'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    categoria = Column(String, index=True)
    data = Column(Date, index=True)
    numerohoras = Column(Integer, index=True)

    local_id = Column(Integer, ForeignKey("locais.id"), nullable=False)
    local = relationship("Local", back_populates="evento")

    organizador_id = Column(Integer, ForeignKey("organizadores.id"), nullable=False)
    organizador = relationship("Organizador", back_populates="evento")

    # Relacionamento N:M com Patrocinadores via Patrocinios
    patrocinio = relationship("Patrocinio", back_populates="evento")

    # Relacionamento N:M com Participantes via Certificados
    certificado = relationship("Certificado", back_populates="evento")
