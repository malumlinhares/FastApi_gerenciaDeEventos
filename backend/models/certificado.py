from sqlalchemy import Column, Integer, ForeignKey, Date, String, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Certificado(Base):
    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    participante_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    autenticador_id = Column(Integer, ForeignKey("autenticadores.id"), nullable=True)  
    data_emissao = Column(Date, nullable=True) 
    codigo_verificacao = Column(String, unique=True, nullable=True) 
    __table_args__ = (
    UniqueConstraint("evento_id", "participante_id", "autenticador_id", name="uq_evento_participante_autenticador"),
)
    evento = relationship("Evento", back_populates="certificado")
    participante = relationship("Participante", back_populates="certificado")
    autenticador = relationship("Autenticador", back_populates="certificado", uselist=False)  
