from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Patrocinio(Base):  
    __tablename__ = 'patrocinios'
    
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, index=True)
    descricao = Column(String, index=True)
    email = Column(String, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False)
    patrocinador_id = Column(Integer, ForeignKey("patrocinadores.id", ondelete="CASCADE"), nullable=False)

    # Relacionamento com Evento (0, n) - Um patrocinio pode estar relacionado a múltiplos eventos
    evento = relationship("Evento", back_populates="patrocinio")

    # Relacionamento com Patrocinador (1, 1) - Cada patrocinio tem um patrocinador
    patrocinador = relationship("Patrocinador", back_populates="patrocinio", single_parent=True)
