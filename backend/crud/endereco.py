from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.endereco import Endereco
from backend.schemas.endereco import EnderecoCreate
from sqlalchemy import text


async def get_all_enderecos(db: AsyncSession):
    result = await db.execute(select(Endereco))  
    return result.scalars().all()  


async def create_endereco(db: AsyncSession, endereco: EnderecoCreate):
    try:
        query = text("""
            INSERT INTO enderecos (rua, cep, numero, complemento, ponto_de_referencia)
            VALUES (:rua, :cep, :numero, :complemento, :ponto_de_referencia)
            RETURNING id, rua, cep, numero,  complemento, ponto_de_referencia
        """)
        params = {
            "rua": endereco.rua,
            "cep": endereco.cep,
            "numero": endereco.numero,
            "complemento": endereco.complemento if endereco.complemento else None,  
            "ponto_de_referencia": endereco.ponto_de_referencia if endereco.ponto_de_referencia else None  
        }

        result = await db.execute(query, params)
        row = result.fetchone()
        await db.commit()

        return {
            "id": row.id,
            "rua": row.rua,
            "cep": row.cep,
            "numero": row.numero,
            "complemento": row.complemento,
            "ponto_de_referencia": row.ponto_de_referencia
        }
    
    except Exception as e:
        await db.rollback()  
        raise e  

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
    db_endereco.complemento = endereco.complemento
    db_endereco.ponto_de_referencia = endereco.ponto_de_referencia
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
    for endereco in db_enderecos:
        await db.refresh(endereco)
    return db_enderecos