from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.participante import Participante
from schemas.participante import ParticipanteCreate
from models.participante import TipoParticipante

async def create_participante(db: AsyncSession, participante: ParticipanteCreate):
    db_participante = Participante(
        nome=participante.nome,
        email=participante.email,
        tipo=TipoParticipante(participante.tipo),
        anuidade = participante.anuidade,
        elegivel_upgrade = participante.elegivel_upgrade

    )
    db.add(db_participante)
    await db.commit()
    await db.refresh(db_participante)
    return db_participante

async def get_participante(db: AsyncSession, participante_id: int):
    result = await db.execute(select(Participante).filter(Participante.id == participante_id))
    participante = result.scalars().first()
    return participante

async def update_participante(db: AsyncSession, participante_id: int, participante: ParticipanteCreate):
    result = await db.execute(select(Participante).filter(Participante.id == participante_id))
    db_participante = result.scalars().first()
    if db_participante is None:
        return None
    db_participante.nome = participante.nome
    db_participante.email = participante.email
    db_participante.tipo = TipoParticipante(participante.tipo)
    db_participante.anuidade = participante.anuidade
    db_participante.elegivel_upgrade = participante.elegivel_upgrade
    
    await db.commit()
    await db.refresh(db_participante)
    return db_participante

async def delete_participante(db: AsyncSession, participante_id: int):
    result = await db.execute(select(Participante).filter(Participante.id == participante_id))
    db_participante = result.scalars().first()
    if db_participante is None:
        return None
    await db.delete(db_participante)
    await db.commit()
    return db_participante
