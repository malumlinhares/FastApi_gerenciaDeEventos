from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Evento(Base):
    __tablename__ = 'eventos'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    categoria = Column(String, index=True)
    data = Column(Date, index=True)
    numerohoras = Column(Integer, index=True)
    organizador_id = Column(Integer, ForeignKey("organizadores.id", ondelete="CASCADE"), nullable=False)
    
    # Relacionamento com Local (se o local for excluído, o evento também será)
    local = relationship("Local", back_populates="evento", cascade="all, delete-orphan")
    patrocinio = relationship("Patrocinio", back_populates="evento", cascade="all, delete-orphan")

    # Relacionamento com Organizador
    organizador = relationship("Organizador", back_populates="evento")  # Alterado para "eventos"
    certificado = relationship("Certificado", back_populates="evento", cascade="all, delete-orphan")
