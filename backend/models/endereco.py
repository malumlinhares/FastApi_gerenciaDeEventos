from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True)
    rua = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)

    # Chave estrangeira para Participante (1:1)
    participante_id = Column(Integer, ForeignKey("participantes.id"), unique=True, nullable=False)
    participante = relationship("Participante", back_populates="endereco", single_parent=True)
