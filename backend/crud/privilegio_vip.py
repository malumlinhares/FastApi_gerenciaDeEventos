from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.privilegio_vip import PrivilegioVip
from schemas.privilegio_vip import PrivilegioVipCreate

async def create_privilegio_vip(db: AsyncSession, privilegio_vip: PrivilegioVipCreate):
    db_privilegio_vip = PrivilegioVip(
        privilegio_id=privilegio_vip.privilegio_id,
        participante_id=privilegio_vip.participante_id
    )
    db.add(db_privilegio_vip)
    await db.commit()
    await db.refresh(db_privilegio_vip)
    return db_privilegio_vip

async def get_privilegio_vip(db: AsyncSession, privilegio_vip_id: int):
    result = await db.execute(select(PrivilegioVip).filter(PrivilegioVip.id == privilegio_vip_id))
    privilegio_vip = result.scalars().first()
    return privilegio_vip

async def update_privilegio_vip(db: AsyncSession, privilegio_vip_id: int, privilegio_vip: PrivilegioVipCreate):
    result = await db.execute(select(PrivilegioVip).filter(PrivilegioVip.id == privilegio_vip_id))
    db_privilegio_vip = result.scalars().first()
    if db_privilegio_vip is None:
        return None
    db_privilegio_vip.privilegio_id = privilegio_vip.privilegio_id
    db_privilegio_vip.participante_id = privilegio_vip.participante_id
    await db.commit()
    await db.refresh(db_privilegio_vip)
    return db_privilegio_vip

async def delete_privilegio_vip(db: AsyncSession, privilegio_vip_id: int):
    result = await db.execute(select(PrivilegioVip).filter(PrivilegioVip.id == privilegio_vip_id))
    db_privilegio_vip = result.scalars().first()
    if db_privilegio_vip is None:
        return None
    await db.delete(db_privilegio_vip)
    await db.commit()
    return db_privilegio_vip
