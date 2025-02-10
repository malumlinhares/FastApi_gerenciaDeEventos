from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint,  DateTime
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Autenticador(Base):
    __tablename__ = "autenticadores"

    id = Column(Integer, primary_key=True)

    # 2 atributos obrigatorios 
    chave_autenticacao = Column(String, nullable=False, unique=True)
    orgao = Column(String, nullable=False, unique=True) 
    # 2 atributos opcionais 
    status = Column(String, nullable=True)
    data_expiracao = Column(DateTime, nullable=True) 


    certificado = relationship("Certificado", back_populates="autenticador", cascade="all, delete-orphan")