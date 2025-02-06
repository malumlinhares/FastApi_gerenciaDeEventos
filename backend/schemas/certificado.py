from pydantic import BaseModel
from typing import List

class CertificadoBase(BaseModel):
    evento_id: int
    participante_id: int
    autenticador_id: int | None

    class Config:
        from_attributes = True

class CertificadoCreate(CertificadoBase):  # Para criação do certificado
    evento_id: int
    participante_id: int
    autenticador_id: int | None

    class Config:
        from_attributes = True

class CertificadoResponse(CertificadoBase):  # Para a resposta com ID
    id: int

class CertificadoBulkCreate(BaseModel):  # Para a criação em massa do Certificado
    certificados: List[CertificadoBase]  

# Esquema para capturar o participante_id como um parâmetro de consulta
class ParticipanteQueryParams(BaseModel):
    participante_id: int

class CertificadoResponse(BaseModel):
    id: int
    evento_id: int
    participante_id: int
    autenticador_id: int | None

