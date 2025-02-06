from pydantic import BaseModel
from typing import List

class PrivilegioVipBase(BaseModel):
    privilegio_id: int
    participante_id: int

    class Config:
        from_attributes = True

class PrivilegioVipCreate(PrivilegioVipBase):  # Para criação do privilégio VIP
    privilegio_id: int
    participante_id: int

    class Config:
        from_attributes = True

class PrivilegioVipResponse(PrivilegioVipBase):  # Para a resposta com ID
    id: int
    privilegio_id: int
    participante_id: int

class PrivilegioVipBulkCreate(BaseModel):  # Para a criação em massa do PrivilegioVip
    privilegios_vips: List[PrivilegioVipBase]  