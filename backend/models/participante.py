from sqlalchemy import Column, Integer, String, ForeignKey
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
    email = Column(String, nullable=False, unique=True)
    tipo = Column(String, nullable=False)  # Pode ser 'vip', 'padrao' 
    anuidade = Column(Integer, nullable=True)
    elegivel_upgrade = Column(Integer, nullable=False)
    

    endereco_id = Column(Integer, ForeignKey('enderecos.id', ondelete="CASCADE"), unique=True)
    endereco = relationship("Endereco", back_populates="participante", uselist=False)  # uselist=False garante a relação 1:1
    # Campos opcionais adicionados
    telefone = Column(String, nullable=True)  # Campo opcional
    responsavel = Column(String, nullable=True)  # Campo opcional

    # Relacionamento N:M com Eventos por meio da tabela Certificados
    certificado = relationship("Certificado", back_populates="participante", cascade="all, delete")
    inscricao = relationship("Inscricao", back_populates="participante", cascade="all, delete-orphan")  # Um participante tem várias inscrições

