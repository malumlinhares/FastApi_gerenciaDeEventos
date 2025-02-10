from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Organizador(Base):
    __tablename__ = 'organizadores'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    cnpj = Column(String, index=True, nullable=False, unique=True)
    telefone = Column(String, nullable=True)  
    nome_contato = Column(String, nullable=True)  

    evento = relationship("Evento", back_populates="organizador")  

