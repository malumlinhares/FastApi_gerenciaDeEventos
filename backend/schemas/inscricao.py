from pydantic import BaseModel

class InscricaoBase(BaseModel):
    status: str
    forma_pagamento: str
    valor: int
    participante_id: int

    class Config:
        from_attributes = True

class InscricaoCreate(InscricaoBase):  # Para criação da inscrição
    status: str
    forma_pagamento: str
    valor: int
    participante_id: int

    class Config:
        from_attributes = True

class InscricaoResponse(InscricaoBase):  # Para a resposta com ID
    numero_inscricao: int
