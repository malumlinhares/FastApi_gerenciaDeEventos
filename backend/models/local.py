from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Local(Base):
    __tablename__ = 'locais'
    
    id = Column(Integer, primary_key=True, index=True)
    cidade = Column(String, index=True, nullable=False)  # Corrigido o erro de digitação "nullabe" para "nullable"
    nome = Column(String, index=True, nullable=False)

    # Campos opcionais
    estado = Column(String, nullable=True)  # O estado do local
    descricao = Column(String, nullable=True)  # Descrição opcional do local

   
    evento = relationship("Evento", back_populates="local",  cascade="all, delete")
    
