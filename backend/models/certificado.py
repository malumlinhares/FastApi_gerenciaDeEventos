from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Certificado(Base):
    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True)

    # Chaves estrangeiras
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    participante_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    autenticador_id = Column(Integer, ForeignKey("autenticadores.id"), nullable=True)

    # Relacionamentos
    evento = relationship("Evento", back_populates="certificado", single_parent=True)
    participante = relationship("Participante", back_populates="certificado", single_parent=True)
    autenticador = relationship("Autenticador", back_populates="certificado", single_parent=True)