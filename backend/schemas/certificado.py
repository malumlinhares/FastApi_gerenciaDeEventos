from pydantic import BaseModel

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
