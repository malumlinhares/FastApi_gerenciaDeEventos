from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint,  Date
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Autenticador(Base):
    __tablename__ = "autenticadores"

    id = Column(Integer, primary_key=True)
    chave_autenticacao = Column(String, nullable=False, unique=True)
    orgao = Column(String, nullable=False, unique=True) 
    status = Column(String, nullable=True)
    data_expiracao = Column(Date, nullable=True) 


    certificado = relationship("Certificado", back_populates="autenticador", cascade="all, delete-orphan")