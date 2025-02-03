from sqlalchemy import Column, Integer, String
from config.database import Base
from sqlalchemy.orm import relationship
from .participante import Participante

class Privilegio(Base):
    __tablename__ = "privilegios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False) # Campo específico para Padrão
    
    privilegio_vip = relationship("PrivilegioVip", back_populates="privilegio")
