from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.evento import Evento
from schemas.evento import EventoCreate

async def create_evento(db: AsyncSession, evento: EventoCreate):
    db_evento = Evento(
        nome=evento.nome,  # Preencher com os dados recebidos
        categoria = evento.categoria, 
        data = evento.data, 
        numerohoras = evento.numerohoras, 
        organizador_id = evento.organizador_id,
    )
    db.add(db_evento)
    await db.commit()
    await db.refresh(db_evento)
    return db_evento  # Retorne o objeto lvento, FastAPI cuidará da conversão

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
