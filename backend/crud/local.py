from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.local import Local
from schemas.local import LocalCreate

async def create_local(db: AsyncSession, local: LocalCreate):
    db_local = Local(
        cidade=local.cidade,  # Preencher com os dados recebidos
        capacidade = local.capacidade, 
        nome = local.nome, 
        evento_id = local.evento_id
    )
    db.add(db_local)
    await db.commit()
    await db.refresh(db_local)
    return db_local  # Retorne o objeto local, FastAPI cuidará da conversão

async def get_local(db: AsyncSession, local_id: int):
    result = await db.execute(
        select(Local).filter(Local.id == local_id)
    )
    local = result.scalars().first()
    return local 


async def update_local(db: AsyncSession, local_id: int, local: LocalCreate):
    result = await db.execute(
        select(Local).filter(Local.id == local_id)
    )
    db_local = result.scalars().first()
    if db_local is None:
        return None
    db_local.cidade = local.cidade
    db_local.capacidade = local.capacidade
    db_local.nome = local.nome
    db_local.evento_id=local.evento_id
    
    await db.commit()
    await db.refresh(db_local)
    return db_local

async def delete_local(db:AsyncSession, local_id: int):
    result = await db.execute(
        select(Local).filter(Local.id==local_id)
    )
    db_local = result.scalars().first()
    if db_local is None:
        return None
    await db.delete(db_local)
    await db.commit()
    return db_local
