from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True)

    # 3 campos obrigatorios
    rua = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)

    #2 campos opcionais
    complemento = Column(String, nullable=True)
    ponto_de_referencia = Column(String, nullable=True)

    # Chave estrangeira para Participante (1:1)
    participante = relationship("Participante", back_populates="endereco", uselist=False)
