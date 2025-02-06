from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.privilegio_vip import PrivilegioVip
from backend.schemas.privilegio_vip import PrivilegioVipCreate
from sqlalchemy import text

# async def create_privilegio_vip(db: AsyncSession, privilegio_vip: PrivilegioVipCreate):
#     db_privilegio_vip = PrivilegioVip(
#         privilegio_id=privilegio_vip.privilegio_id,
#         participante_id=privilegio_vip.participante_id
#     )
#     db.add(db_privilegio_vip)
#     await db.commit()
#     await db.refresh(db_privilegio_vip)
#     return db_privilegio_vip



async def create_privilegio_vip(db: AsyncSession, privilegio_vip: PrivilegioVipCreate):
    query = text("""
        INSERT INTO privilegios_vip ( participante_id, privilegio_id)
        VALUES (:participante_id, :privilegio_id)
        RETURNING id,  participante_id, privilegio_id
    """)
    params = {
        "participante_id": privilegio_vip.participante_id, 
        "privilegio_id": privilegio_vip.privilegio_id
    }
    result = await db.execute(query, params)
    row = result.fetchone()
    await db.commit()
    return {
        "participante_id": row.participante_id, 
        "privilegio_id": row.privilegio_id
    }


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

async def bulk_create_privilegios_vip(db: AsyncSession, privilegios_vips: list[PrivilegioVipCreate]):
    db_privilegios_vips = [PrivilegioVip(**privilegio_vip.model_dump()) for privilegio_vip in privilegios_vips]
    db.add_all(db_privilegios_vips)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for privilegio_vip in db_privilegios_vips:
        await db.refresh(privilegio_vip)
    return db_privilegios_vips

