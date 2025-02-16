from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.inscricao import Inscricao
from backend.schemas.inscricao import InscricaoCreate
from sqlalchemy import text


async def get_all_inscricoes(db: AsyncSession):
    result = await db.execute(select(Inscricao))  
    return result.scalars().all() 


async def create_inscricao(db: AsyncSession, inscricao: InscricaoCreate):
    try:
        query = text("""
            INSERT INTO inscricao (status, forma_pagamento, valor, participante_id, data_pagamento, observacao)
            VALUES (COALESCE(:status, 'Pendente'), :forma_pagamento, :valor, :participante_id, :data_pagamento, :observacao)
            RETURNING numero_inscricao, status, forma_pagamento, valor, participante_id, data_pagamento, observacao
        """)
        params = {
            "status": inscricao.status or 'Pendente',  
            "forma_pagamento": inscricao.forma_pagamento,
            "valor": inscricao.valor,
            "participante_id": inscricao.participante_id,
            "data_pagamento": inscricao.data_pagamento,  
            "observacao": inscricao.observacao  
        }
        result = await db.execute(query, params)
        row = result.fetchone()
        await db.commit()
        return {
            "numero_inscricao": row.numero_inscricao,
            "status": row.status,
            "forma_pagamento": row.forma_pagamento,
            "valor": row.valor,
            "participante_id": row.participante_id,
            "data_pagamento": row.data_pagamento, 
            "observacao": row.observacao  
        }
    except Exception as e:
        await db.rollback()  
        raise e  


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
    db_inscricao.data_pagamento = inscricao.data_pagamento
    db_inscricao.observacao = inscricao.observacao
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


async def bulk_create_inscricao(db: AsyncSession, inscricoes: list[InscricaoCreate]):
    db_inscricoes = [Inscricao(**inscricao.model_dump()) for inscricao in inscricoes]
    db.add_all(db_inscricoes)
    await db.commit()
    for inscricao in db_inscricoes:
        await db.refresh(inscricao)
    return db_inscricoes