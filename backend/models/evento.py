# backend/models/evento.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Evento(Base):
    __tablename__ = 'eventos'
    
    id = Column(Integer, primary_key=True, index=True)

    # atributos obrigatorios
    nome = Column(String, index=True, nullable=False)
    categoria = Column(String, index=True, nullable=False)
    data = Column(Date, index=True, nullable=False)
    numerohoras = Column(Integer, index=True, nullable=False)
    local_id = Column(Integer, ForeignKey("locais.id"), nullable=False)
    organizador_id = Column(Integer, ForeignKey("organizadores.id"), nullable=False)
    
    #atributos opcinais
    descricao = Column(String, nullable=True)  # Opcional - Descrição do evento
    limite_participantes = Column(Integer, nullable=True)  


    local = relationship("Local", back_populates="evento")
    organizador = relationship("Organizador", back_populates="evento")
    # Relacionamento N:M com Patrocinadores via Patrocinios
    patrocinio = relationship("Patrocinio", back_populates="evento")
    # Relacionamento N:M com Participantes via Certificados
    certificado = relationship("Certificado", back_populates="evento")
