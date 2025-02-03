from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.inscricao import Inscricao
from schemas.inscricao import InscricaoCreate

async def create_inscricao(db: AsyncSession, inscricao: InscricaoCreate):
    db_inscricao = Inscricao(
        status=inscricao.status,
        forma_pagamento=inscricao.forma_pagamento,
        valor=inscricao.valor,
        participante_id=inscricao.participante_id,
    )
    db.add(db_inscricao)
    await db.commit()
    await db.refresh(db_inscricao)
    return db_inscricao

async def get_inscricao(db: AsyncSession, inscricao_id: int):
    result = await db.execute(select(Inscricao).filter(Inscricao.numero_inscricao == inscricao_id))
    inscricao = result.scalars().first()
    return inscricao

async def update_inscricao(db: AsyncSession, inscricao_id: int, inscricao: InscricaoCreate):
    result = await db.execute(select(Inscricao).filter(Inscricao.numero_inscricao == inscricao_id))
    db_inscricao = result.scalars().first()
    if db_inscricao is None:
        return None
    db_inscricao.status = inscricao.status
    db_inscricao.forma_pagamento = inscricao.forma_pagamento
    db_inscricao.valor = inscricao.valor
    db_inscricao.participante_id = inscricao.participante_id
    await db.commit()
    await db.refresh(db_inscricao)
    return db_inscricao

async def delete_inscricao(db: AsyncSession, inscricao_id: int):
    result = await db.execute(select(Inscricao).filter(Inscricao.numero_inscricao == inscricao_id))
    db_inscricao = result.scalars().first()
    if db_inscricao is None:
        return None
    await db.delete(db_inscricao)
    await db.commit()
    return db_inscricao
