from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from datetime import date

class CertificadoBase(BaseModel):
    evento_id: int
    participante_id: int
    autenticador_id: Optional[int] = None  

    class Config:
        from_attributes = True

class CertificadoCreate(CertificadoBase):  
    data_emissao: Optional[date] = None  
    codigo_verificacao: Optional[str] = None  

class CertificadoResponse(CertificadoBase):  
    id: int
    data_emissao: Optional[date] = None
    codigo_verificacao: Optional[str] = None

class CertificadoBulkCreate(BaseModel):  
    certificados: List[CertificadoCreate]  


class ParticipanteQueryParams(BaseModel):
    participante_id: int
