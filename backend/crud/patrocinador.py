from sqlalchemy.ext.asyncio import AsyncSession
from models.patrocinador import Patrocinador, TipoPatrocinador
from schemas.patrocinador import PatrocinadorCreate
from sqlalchemy.future import select

# Função para criar patrocinador
async def create_patrocinador(db: AsyncSession, patrocinador: PatrocinadorCreate):
    db_patrocinador = Patrocinador(
        nome=patrocinador.nome,
        email=patrocinador.email,
        tipo=TipoPatrocinador(patrocinador.tipo),  # Convertendo para o tipo Enum
        orgao_responsavel=patrocinador.orgao_responsavel,
        responsavel_comercial=patrocinador.responsavel_comercial,
    )
    db.add(db_patrocinador)
    await db.commit()
    await db.refresh(db_patrocinador)
    return db_patrocinador

# Função para buscar patrocinador
async def get_patrocinador(db: AsyncSession, patrocinador_id: int):
    result = await db.execute(
        select(Patrocinador).filter(Patrocinador.id == patrocinador_id)
    )
    patrocinador = result.scalars().first()
    return patrocinador

# Função para atualizar patrocinador
async def update_patrocinador(db: AsyncSession, patrocinador_id: int, patrocinador: PatrocinadorCreate):
    result = await db.execute(
        select(Patrocinador).filter(Patrocinador.id == patrocinador_id)
    )
    db_patrocinador = result.scalars().first()
    if db_patrocinador is None:
        return None

    db_patrocinador.nome = patrocinador.nome
    db_patrocinador.email = patrocinador.email
    db_patrocinador.tipo = TipoPatrocinador(patrocinador.tipo)  # Atualizando tipo (Enum)
    db_patrocinador.orgao_responsavel = patrocinador.orgao_responsavel
    db_patrocinador.responsavel_comercial = patrocinador.responsavel_comercial

    await db.commit()
    await db.refresh(db_patrocinador)
    return db_patrocinador

# Função para deletar patrocinador
async def delete_patrocinador(db: AsyncSession, patrocinador_id: int):
    result = await db.execute(
        select(Patrocinador).filter(Patrocinador.id == patrocinador_id)
    )
    db_patrocinador = result.scalars().first()
    if db_patrocinador is None:
        return None
    await db.delete(db_patrocinador)
    await db.commit()

    return db_patrocinador
