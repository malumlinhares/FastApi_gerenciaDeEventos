from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from backend.config.database import Base
import enum

class TipoPatrocinador(str, enum.Enum):
    publico = "publico"
    privado = "privado"

class Patrocinador(Base):  
    __tablename__ = "patrocinadores"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    tipo = Column(Enum(TipoPatrocinador, name="tipo_patrocinador", create_type=True), nullable=False)
    orgao_responsavel = Column(String, nullable=True)
    responsavel_comercial = Column(String, nullable=True)  
    telefone = Column(String, nullable=True)  
    nome_responsavel = Column(String, nullable=True) 


    patrocinio = relationship("Patrocinio", back_populates="patrocinador")

    __mapper_args__ = {
        'polymorphic_on': tipo,
        'with_polymorphic': '*'
    }
