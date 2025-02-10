from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Organizador(Base):
    __tablename__ = 'organizadores'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    cnpj = Column(String, index=True, nullable=False, unique=True)
    
    # 2 atributos opcionais
    telefone = Column(String, nullable=True)  # Atributo opcional
    nome_contato = Column(String, nullable=True)  # Atributo opcional

    
    # Relacionamento de volta para Evento (lado "um")
    evento = relationship("Evento", back_populates="organizador")  # uselist=False para garantir um único evento por organizador

