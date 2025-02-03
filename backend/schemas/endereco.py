from pydantic import BaseModel

class EnderecoBase(BaseModel):
    rua: str
    cep: str
    numero: int
    participante_id: int

    class Config:
        from_attributes = True

class EnderecoCreate(EnderecoBase):  # Para criação do endereço
    rua: str
    cep: str
    numero: int
    participante_id: int

    class Config:
        from_attributes = True

class EnderecoResponse(EnderecoBase):  # Para a resposta com ID
    id: int
