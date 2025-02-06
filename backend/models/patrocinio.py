# backend/models/patrocinio.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Patrocinio(Base):  
    __tablename__ = 'patrocinios'
    
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, index=True)
    descricao = Column(String, index=True)
    email = Column(String, index=True)
    
    evento_id = Column(Integer, ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False)
    patrocinador_id = Column(Integer, ForeignKey("patrocinadores.id", ondelete="CASCADE"), nullable=False)

    # Relacionamentos
    evento = relationship("Evento", back_populates="patrocinio")
    patrocinador = relationship("Patrocinador", back_populates="patrocinio")
