from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base
from typing import Optional

class Patrocinio(Base):
    __tablename__ = 'patrocinios'
    
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, index=True, nullable=False)
    descricao = Column(String, index=True, nullable=False)
    
    evento_id = Column(Integer, ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False)
    patrocinador_id = Column(Integer, ForeignKey("patrocinadores.id", ondelete="CASCADE"), nullable=False)
    
    # Atributos opcionais
    status = Column(String, nullable=True)  # Atributo opcional para status (por exemplo, "ativo", "inativo")
    observacao = Column(String, nullable=True)  # Atributo opcional para observações adicionais

    # Relacionamentos
    evento = relationship("Evento", back_populates="patrocinio")
    patrocinador = relationship("Patrocinador", back_populates="patrocinio")
