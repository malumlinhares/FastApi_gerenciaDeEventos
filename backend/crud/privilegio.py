from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.privilegio import Privilegio
from schemas.privilegio import PrivilegioCreate

async def create_privilegio(db: AsyncSession, privilegio: PrivilegioCreate):
    db_privilegio = Privilegio(
        nome=privilegio.nome,
        descricao=privilegio.descricao
    )
    db.add(db_privilegio)
    await db.commit()
    await db.refresh(db_privilegio)
    return db_privilegio

async def get_privilegio(db: AsyncSession, privilegio_id: int):
    result = await db.execute(select(Privilegio).filter(Privilegio.id == privilegio_id))
    privilegio = result.scalars().first()
    return privilegio

async def update_privilegio(db: AsyncSession, privilegio_id: int, privilegio: PrivilegioCreate):
    result = await db.execute(select(Privilegio).filter(Privilegio.id == privilegio_id))
    db_privilegio = result.scalars().first()
    if db_privilegio is None:
        return None
    db_privilegio.nome = privilegio.nome
    db_privilegio.descricao = privilegio.descricao
    await db.commit()
    await db.refresh(db_privilegio)
    return db_privilegio

async def delete_privilegio(db: AsyncSession, privilegio_id: int):
    result = await db.execute(select(Privilegio).filter(Privilegio.id == privilegio_id))
    db_privilegio = result.scalars().first()
    if db_privilegio is None:
        return None
    await db.delete(db_privilegio)
    await db.commit()
    return db_privilegio
