# from pydantic import BaseModel
# from typing import List

# class AutenticadorBase(BaseModel):
#     orgao: str

#     class Config:
#         from_attributes = True

# class AutenticadorCreate(AutenticadorBase):  # Para criação do autenticador
#     orgao: str

#     class Config:
#         from_attributes = True

# class AutenticadorResponse(AutenticadorBase):  # Para a resposta com ID
#     id: int

# class AutenticadorBulkCreate(BaseModel):  # Para a criação em massa do Autenticador
#     autenticadores: List[AutenticadorBase]  

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AutenticadorBase(BaseModel):
    orgao: str
    status: str

    class Config:
        from_attributes = True

class AutenticadorCreate(AutenticadorBase):  # Para criação do autenticador
    chave_autenticacao: str
    data_expiracao: Optional[datetime] = None  # Opcional

class AutenticadorResponse(AutenticadorBase):  # Para a resposta com ID
    id: int
    chave_autenticacao: str
    data_expiracao: Optional[datetime] = None  # Opcional

class AutenticadorBulkCreate(BaseModel):  # Para a criação em massa do Autenticador
    autenticadores: List[AutenticadorCreate]
