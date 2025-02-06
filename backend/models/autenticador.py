from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Autenticador(Base):
    __tablename__ = "autenticadores"

    id = Column(Integer, primary_key=True)
    orgao = Column(String, nullable=False)  # Obrigatório ter um órgão

    # Relacionamento com Certificado
    certificado = relationship("Certificado", back_populates="autenticador", cascade="all, delete-orphan")