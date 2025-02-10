# from pydantic import BaseModel
# from typing import List, Optional

# # class InscricaoBase(BaseModel):
# #     status: str
# #     forma_pagamento: str
# #     valor: int
# #     participante_id: int

# #     class Config:
# #         from_attributes = True


# class InscricaoBase(BaseModel):
#     status: str = 'Pendente'  # Definir padrão no Python
#     forma_pagamento: str
#     valor: int
#     participante_id: int

#     class Config:
#         from_attributes = True

# class InscricaoCreate(InscricaoBase):  # Para criação da inscrição
#     status: str
#     forma_pagamento: str
#     valor: int
#     participante_id: int

#     class Config:
#         from_attributes = True

# class InscricaoResponse(InscricaoBase):  # Para a resposta com ID
#     numero_inscricao: int
#     status: str
#     forma_pagamento: str
#     valor: int
#     participante_id: int

# class InscricaoBulkCreate(BaseModel):  # Para a criação em massa do Inscricao
#     inscricoes: List[InscricaoBase]  
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class InscricaoBase(BaseModel):
    status: str = 'Pendente'  # Definir padrão no Python
    forma_pagamento: str
    valor: int
    participante_id: int
    data_pagamento: Optional[date] = None  # Campo opcional
    observacao: Optional[str] = None  # Campo opcional

    class Config:
        from_attributes = True

class InscricaoCreate(InscricaoBase):  # Para criação da inscrição
    status: str
    forma_pagamento: str
    valor: int
    participante_id: int
    data_pagamento: Optional[date] = None  # Campo opcional
    observacao: Optional[str] = None  # Campo opcional

    class Config:
        from_attributes = True

class InscricaoResponse(InscricaoBase):  # Para a resposta com ID
    numero_inscricao: int
    status: str
    forma_pagamento: str
    valor: int
    participante_id: int
    data_pagamento: Optional[date] = None  # Campo opcional
    observacao: Optional[str] = None  # Campo opcional

class InscricaoBulkCreate(BaseModel):  # Para a criação em massa da Inscrição
    inscricoes: List[InscricaoBase]  
