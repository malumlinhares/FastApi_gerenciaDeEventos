from sqlalchemy.ext.asyncio import AsyncSession
from models.patrocinio import Patrocinio
from schemas.patrocinio import PatrocinioCreate
from sqlalchemy.future import select

async def create_patrocinio(db: AsyncSession, patrocinio: PatrocinioCreate):
    db_patrocinio = Patrocinio(
        valor=patrocinio.valor, descricao = patrocinio.descricao, 
        patrocinador_id=patrocinio.patrocinador_id, 
        evento_id=patrocinio.evento_id)
    db.add(db_patrocinio)
    await db.commit()
    await db.refresh(db_patrocinio)
    return db_patrocinio

async def get_patrocinio(db: AsyncSession, patrocinio_id: int):
    # Aqui você faz a consulta para buscar o patrocinio
    result = await db.execute(
        select(Patrocinio).filter(Patrocinio.id == patrocinio_id)
    )
    patrocinio = result.scalars().first()
    return patrocinio

async def update_patrocinio(db: AsyncSession, patrocinio_id: int, patrocinio: PatrocinioCreate):
    result = await db.execute(
        select(Patrocinio).filter(Patrocinio.id == patrocinio_id)
    )
    db_patrocinio = result.scalars().first()
    if db_patrocinio is None:
        return None
    
    db_patrocinio.valor = patrocinio.valor
    db_patrocinio.descricao = patrocinio.descricao
    db_patrocinio.evento_id = patrocinio.evento_id
    db_patrocinio.patrocinador_id = patrocinio.patrocinador_id

    await db.commit()
    await db.refresh(db_patrocinio)
    return db_patrocinio

async def delete_patrocinio(db:AsyncSession, patrocinio_id: int):
    result = await db.execute(
        select(Patrocinio).filter(Patrocinio.id==patrocinio_id)
    )
    db_patrocinio = result.scalars().first()
    if db_patrocinio is None:
        return None
    await db.delete(db_patrocinio)
    await db.commit()

    return db_patrocinio