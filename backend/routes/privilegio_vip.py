from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.privilegio_vip import PrivilegioVipCreate, PrivilegioVipResponse
from backend.crud.privilegio_vip import create_privilegio_vip, get_privilegio_vip, update_privilegio_vip, delete_privilegio_vip

router = APIRouter()

@router.post("/", response_model=PrivilegioVipResponse)
async def create_privilegio_vip_api(privilegio_vip: PrivilegioVipCreate, db: AsyncSession = Depends(get_db)):
    return await create_privilegio_vip(db=db, privilegio_vip=privilegio_vip)

@router.get("/{privilegio_vip_id}", response_model=PrivilegioVipResponse)
async def read_privilegio_vip_api(privilegio_vip_id: int, db: AsyncSession = Depends(get_db)):
    db_privilegio_vip = await get_privilegio_vip(db=db, privilegio_vip_id=privilegio_vip_id)
    if db_privilegio_vip is None:
        raise HTTPException(status_code=404, detail="Privilégio VIP não encontrado")
    return db_privilegio_vip

@router.put("/{privilegio_vip_id}", response_model=PrivilegioVipResponse)
async def update_privilegio_vip_api(
    privilegio_vip_id: int,
    privilegio_vip: PrivilegioVipCreate,
    db: AsyncSession = Depends(get_db)
):
    db_privilegio_vip = await update_privilegio_vip(db=db, privilegio_vip_id=privilegio_vip_id, privilegio_vip=privilegio_vip)
    if db_privilegio_vip is None:
        raise HTTPException(status_code=404, detail="Privilégio VIP não encontrado")
    return db_privilegio_vip

@router.delete("/{privilegio_vip_id}", response_model=PrivilegioVipResponse)
async def delete_privilegio_vip_api(
    privilegio_vip_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_privilegio_vip = await delete_privilegio_vip(db=db, privilegio_vip_id=privilegio_vip_id)
    if db_privilegio_vip is None:
        raise HTTPException(status_code=404, detail="Privilégio VIP não encontrado")
    return db_privilegio_vip
