from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.evento import Evento
from backend.schemas.evento import EventoCreate, EventoResponse
from sqlalchemy import text

#usando biblioteca

# async def create_evento(db: AsyncSession, evento: EventoCreate):
#     db_evento = Evento(
#         nome=evento.nome,  # Preencher com os dados recebidos
#         categoria = evento.categoria, 
#         data = evento.data, 
#         numerohoras = evento.numerohoras, 
#         local_id = evento.local_id,
#         organizador_id = evento.organizador_id
#     )
#     db.add(db_evento)
#     await db.commit()
#     await db.refresh(db_evento)
#     return db_evento  # Retorne o objeto lvento, FastAPI cuidará da conversão

# usando sql nativo
async def create_evento(db: AsyncSession, evento: EventoCreate):
    query = text("""
        INSERT INTO eventos (nome, categoria, data, numerohoras, local_id, organizador_id)
        VALUES (:nome, :categoria, :data, :numerohoras, :local_id, :organizador_id)
        RETURNING id, nome, categoria, data, numerohoras, local_id, organizador_id
    """)
    params = {
        "nome": evento.nome,
        "categoria": evento.categoria,
        "data": evento.data,
        "numerohoras": evento.numerohoras,
        "local_id": evento.local_id,
        "organizador_id": evento.organizador_id
    }
    result = await db.execute(query, params)
    row = result.fetchone()
    await db.commit()
    return {
        "id": row.id,
        "nome": row.nome,
        "categoria": row.categoria,
        "data": row.data,
        "numerohoras": row.numerohoras,
        "local_id": row.local_id,
        "organizador_id": row.organizador_id
    }



async def get_evento(db: AsyncSession, evento_id: int):
    result = await db.execute(
        select(Evento).filter(Evento.id == evento_id)
    )
    evento = result.scalars().first()
    return evento 



async def update_evento(db: AsyncSession, evento_id: int, evento: EventoCreate):
    result = await db.execute(
        select(Evento).filter(Evento.id == evento_id)
    )
    db_evento = result.scalars().first()
    if db_evento is None:
        return None
    db_evento.nome = evento.nome
    db_evento.categoria = evento.categoria
    db_evento.data = evento.data
    db_evento.numerohoras = evento.numerohoras
    db_evento.local_id = evento.local_id
    db_evento.organizador_id=evento.organizador_id
    
    await db.commit()
    await db.refresh(db_evento)
    return db_evento

async def delete_evento(db:AsyncSession, evento_id: int):
    result = await db.execute(
        select(Evento).filter(Evento.id==evento_id)
    )
    db_evento = result.scalars().first()
    if db_evento is None:
        return None
    await db.delete(db_evento)
    await db.commit()
    return db_evento


async def bulk_create_evento(db: AsyncSession, eventos: list[EventoCreate]):
    db_eventos = [Evento(**evento.model_dump()) for evento in eventos]
    db.add_all(db_eventos)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for evento in db_eventos:
        await db.refresh(evento)
    return db_eventos


