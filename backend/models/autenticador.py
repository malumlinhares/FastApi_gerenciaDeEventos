from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class Autenticador(Base):
    __tablename__ = "autenticadores"

    id = Column(Integer, primary_key=True)
    orgao = Column(String, nullable=False)

    # Relacionamento 1:N com Certificado
    certificado = relationship("Certificado", back_populates="autenticador")
