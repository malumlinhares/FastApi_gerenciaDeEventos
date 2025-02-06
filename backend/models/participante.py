from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.config.database import Base
import enum

class TipoParticipante(str, enum.Enum):
    vip = "vip"
    padrao = "padrao"

class Participante(Base):
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # Pode ser 'vip', 'padrao' ou outro tipo
    anuidade = Column(Integer, nullable=True)
    elegivel_upgrade = Column(Integer, nullable=False)

    # Relacionamento N:M com Eventos por meio da tabela Certificados
    certificado = relationship("Certificado", back_populates="participante", cascade="all, delete")
    #1:1
    endereco = relationship("Endereco", back_populates="participante", uselist=False)

    inscricao = relationship("Inscricao", back_populates="participante", cascade="all, delete-orphan")  # Um participante tem várias inscrições

    # privilegio_vip = relationship("PrivilegioVIP", back_populates="participante")  # Um participante pode ter 0 ou N privilégios VIP