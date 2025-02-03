from pydantic import BaseModel

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
