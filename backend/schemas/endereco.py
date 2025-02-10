# from pydantic import BaseModel
# from typing import List

# class EnderecoBase(BaseModel):
#     rua: str
#     cep: str
#     numero: int
#     participante_id: int

#     class Config:
#         from_attributes = True

# class EnderecoCreate(EnderecoBase):  # Para criação do endereço
#     rua: str
#     cep: str
#     numero: int
#     participante_id: int

#     class Config:
#         from_attributes = True

# class EnderecoResponse(EnderecoBase):  # Para a resposta com ID
#     id: int

# class EnderecoBulkCreate(BaseModel):  # Para a criação em massa do Endereco
#     endercos: List[EnderecoBase]  

from pydantic import BaseModel
from typing import List, Optional

class EnderecoBase(BaseModel):
    rua: str
    cep: str
    numero: int
    complemento: Optional[str] = None  # Opcional
    ponto_de_referencia: Optional[str] = None  # Opcional

    class Config:
        from_attributes = True

class EnderecoCreate(EnderecoBase):  # Para criação do endereço
    pass  # Já herda tudo do EnderecoBase

class EnderecoResponse(EnderecoBase):  # Para a resposta com ID
    id: int

class EnderecoBulkCreate(BaseModel):  # Para criação em massa do Endereco
    enderecos: List[EnderecoBase]  # Corrigido nome da variável
