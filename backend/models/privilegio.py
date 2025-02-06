from sqlalchemy import Column, Integer, String
from backend.config.database import Base
from sqlalchemy.orm import relationship

class Privilegio(Base):
    __tablename__ = "privilegios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False) # Campo específico para Padrão
    
    privilegio_vip = relationship("PrivilegioVip", back_populates="privilegio", cascade="all, delete")
