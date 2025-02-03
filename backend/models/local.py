from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Local(Base):
    __tablename__ = 'locais'
    
    id = Column(Integer, primary_key=True, index=True)
    cidade = Column(String, index=True)
    capacidade = Column(Integer, index = True)
    nome = Column(String, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False)
   
    evento = relationship("Evento", back_populates="local", single_parent=True)
