from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Certificado(Base):
    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True)

    # Chaves estrangeiras representando a relação N:M entre Evento e Participante
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    participante_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    
    autenticador_id = Column(Integer, ForeignKey("autenticadores.id"), nullable=True)  # Pode ser nulo se não tiver autenticador

    # Relacionamentos
    evento = relationship("Evento", back_populates="certificado")
    participante = relationship("Participante", back_populates="certificado")
    autenticador = relationship("Autenticador", back_populates="certificado", uselist=False)  # Cada certificado pode ter um autenticador
