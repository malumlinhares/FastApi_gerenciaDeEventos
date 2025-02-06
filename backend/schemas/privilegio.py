from pydantic import BaseModel
from typing import List

class PrivilegioBase(BaseModel):
    nome: str
    descricao: str

    class Config:
        from_attributes = True

class PrivilegioCreate(PrivilegioBase):  # Para criação do privilégio
    nome: str
    descricao: str

    class Config:
        from_attributes = True

class PrivilegioResponse(PrivilegioBase):  # Para a resposta com ID
    id: int
    nome: str
    descricao: str

class PrivilegioBulkCreate(BaseModel):  # Para a criação em massa do Privilegio
    privilegios: List[PrivilegioBase]  