from pydantic import BaseModel
from typing import List

class AutenticadorBase(BaseModel):
    orgao: str

    class Config:
        from_attributes = True

class AutenticadorCreate(AutenticadorBase):  # Para criação do autenticador
    orgao: str

    class Config:
        from_attributes = True

class AutenticadorResponse(AutenticadorBase):  # Para a resposta com ID
    id: int

class AutenticadorBulkCreate(BaseModel):  # Para a criação em massa do Autenticador
    autenticadores: List[AutenticadorBase]  