from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.endereco import Endereco
from backend.schemas.endereco import EnderecoCreate
from sqlalchemy import text

#usando funcao pronta
# async def create_endereco(db: AsyncSession, endereco: EnderecoCreate):
#     db_endereco = Endereco(
#         rua=endereco.rua,
#         cep=endereco.cep,
#         numero=endereco.numero,
#         participante_id=endereco.participante_id
#     )
#     db.add(db_endereco)
#     await db.commit()
#     await db.refresh(db_endereco)
#     return db_endereco

# usando sql nativo
async def create_endereco(db: AsyncSession, endereco: EnderecoCreate):
    query = text("""
        INSERT INTO enderecos (rua, cep, numero, participante_id)
        VALUES (:rua, :cep, :numero, :participante_id)
        RETURNING id, rua, cep, numero, participante_id
    """)
    params = {
        "rua": endereco.rua,
        "cep": endereco.cep,
        "numero": endereco.numero,
        "participante_id": endereco.participante_id
    }
    result = await db.execute(query, params)
    row = result.fetchone()
    await db.commit()
    return {
        "id": row.id,
        "rua": row.rua,
        "cep": row.cep,
        "numero": row.numero,
        "participante_id": row.participante_id
    }

async def get_endereco(db: AsyncSession, endereco_id: int):
    result = await db.execute(select(Endereco).filter(Endereco.id == endereco_id))
    endereco = result.scalars().first()
    return endereco

async def update_endereco(db: AsyncSession, endereco_id: int, endereco: EnderecoCreate):
    result = await db.execute(select(Endereco).filter(Endereco.id == endereco_id))
    db_endereco = result.scalars().first()
    if db_endereco is None:
        return None
    db_endereco.rua = endereco.rua
    db_endereco.cep = endereco.cep
    db_endereco.numero = endereco.numero
    db_endereco.participante_id = endereco.participante_id
    await db.commit()
    await db.refresh(db_endereco)
    return db_endereco

async def delete_endereco(db: AsyncSession, endereco_id: int):
    result = await db.execute(select(Endereco).filter(Endereco.id == endereco_id))
    db_endereco = result.scalars().first()
    if db_endereco is None:
        return None
    await db.delete(db_endereco)
    await db.commit()
    return db_endereco

async def bulk_create_endereco(db: AsyncSession, enderecos: list[EnderecoCreate]):
    db_enderecos = [Endereco(**endereco.model_dump()) for endereco in enderecos]
    db.add_all(db_enderecos)
    await db.commit()
    # Atualiza os objetos para garantir dados consistentes
    for endereco in db_enderecos:
        await db.refresh(endereco)
    return db_enderecos