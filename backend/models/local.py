from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Local(Base):
    __tablename__ = 'locais'
    
    id = Column(Integer, primary_key=True, index=True)
    cidade = Column(String, index=True, nullable=False)  
    nome = Column(String, index=True, nullable=False)
    estado = Column(String, nullable=True)  
    descricao = Column(String, nullable=True) 

   
    evento = relationship("Evento", back_populates="local",  cascade="all, delete")
    
