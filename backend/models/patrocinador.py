# backend/models/patrocinador.py
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from config.database import Base
import enum

# Enum corrigido: Herdando de str para evitar problemas no PostgreSQL
class TipoPatrocinador(str, enum.Enum):
    publico = "publico"
    privado = "privado"

class Patrocinador(Base):  
    __tablename__ = "patrocinadores"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tipo = Column(Enum(TipoPatrocinador, name="tipo_patrocinador", create_type=True), nullable=False)  # Enum correto
    orgao_responsavel = Column(String, nullable=True)
    responsavel_comercial = Column(String, nullable=True)  # Somente preenchido para patrocinadores do tipo "privado"
    
    # Relacionamento com Patrocínio (0, n)
    patrocinio = relationship("Patrocinio", back_populates="patrocinador")

    __mapper_args__ = {
        'polymorphic_on': tipo,
        'with_polymorphic': '*'
    }
