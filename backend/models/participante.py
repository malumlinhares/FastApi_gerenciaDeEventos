# backend/models/participante.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from config.database import Base
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


    
    # Relacionamentos
    privilegio_vip = relationship("PrivilegioVip", back_populates="participante", cascade="all, delete-orphan")
    inscricao = relationship("Inscricao", back_populates="participante")
    endereco = relationship("Endereco", uselist=False, back_populates="participante", single_parent=True)
    certificado = relationship("Certificado", back_populates="participante",  cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_on': tipo,
        'with_polymorphic': '*'
    }
