from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class Organizador(Base):
    __tablename__ = 'organizadores'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, index=True)
    cnpj = Column(String, index=True)
    
    # Relacionamento de volta para Evento (lado "um")
    evento = relationship("Evento", back_populates="organizador", cascade="all, delete-orphan")  # uselist=False para garantir um único evento por organizador

