from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.patrocinador import Patrocinador, TipoPatrocinador
from backend.schemas.patrocinador import PatrocinadorCreate
from sqlalchemy.future import select
from sqlalchemy import text

async def get_all_patrocinadores(db: AsyncSession):
    result = await db.execute(select(Patrocinador)) 
    return result.scalars().all() 

async def create_patrocinador(db: AsyncSession, patrocinador: PatrocinadorCreate):
    try:
        query = text("""
            INSERT INTO patrocinadores (nome, email, tipo, orgao_responsavel, responsavel_comercial, telefone, nome_responsavel)
            VALUES (:nome, :email, :tipo, :orgao_responsavel, :responsavel_comercial, :telefone, :nome_responsavel)
            RETURNING id, nome, email, tipo, orgao_responsavel, responsavel_comercial, telefone, nome_responsavel
        """)
        params = {
            "nome": patrocinador.nome,
            "email": patrocinador.email,
            "tipo": patrocinador.tipo,
            "orgao_responsavel": patrocinador.orgao_responsavel,
            "responsavel_comercial": patrocinador.responsavel_comercial,
            "telefone": patrocinador.telefone, 
            "nome_responsavel": patrocinador.nome_responsavel   
        }
        result = await db.execute(query, params)
        row = result.fetchone()
        await db.commit()

        return {
            "id": row.id,
            "nome": row.nome,
            "email": row.email,
            "tipo": row.tipo,
            "orgao_responsavel": row.orgao_responsavel,
            "responsavel_comercial": row.responsavel_comercial,
            "telefone": row.telefone,  
            "nome_responsavel": row.nome_responsavel  
        }
    except Exception as e:
        await db.rollback()  
        raise e  


async def get_patrocinador(db: AsyncSession, patrocinador_id: int):
    result = await db.execute(
        select(Patrocinador).filter(Patrocinador.id == patrocinador_id)
    )
    patrocinador = result.scalars().first()
    return patrocinador


async def update_patrocinador(db: AsyncSession, patrocinador_id: int, patrocinador: PatrocinadorCreate):
    result = await db.execute(
        select(Patrocinador).filter(Patrocinador.id == patrocinador_id)
    )
    db_patrocinador = result.scalars().first()
    if db_patrocinador is None:
        return None
    db_patrocinador.nome = patrocinador.nome
    db_patrocinador.email = patrocinador.email
    db_patrocinador.tipo = TipoPatrocinador(patrocinador.tipo)  
    db_patrocinador.orgao_responsavel = patrocinador.orgao_responsavel
    db_patrocinador.responsavel_comercial = patrocinador.responsavel_comercial
    db_patrocinador.telefone = patrocinador.telefone
    db_patrocinador.nome_responsavel = patrocinador.nome_responsavel

    await db.commit()
    await db.refresh(db_patrocinador)
    return db_patrocinador

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

async def bulk_create_patrocinador(db: AsyncSession, patrocinadores: list[PatrocinadorCreate]):
    db_patrocinadores = [Patrocinador(**patrocinador.model_dump()) for patrocinador in patrocinadores]
    db.add_all(db_patrocinadores)
    await db.commit()
    for patrocinador in db_patrocinadores:
        await db.refresh(patrocinador)
    return db_patrocinadores

# pesquisar patrocinador por nome - substring
async def search_patrocinador_by_name(db: AsyncSession, nome_substring: str):
    query = text("""
        SELECT * 
        FROM patrocinadores
        WHERE nome ILIKE :nome_substring
    """)
    result = await db.execute(query, {"nome_substring": f"%{nome_substring}%"})
    patrocinadores = result.fetchall()
    return patrocinadores

#retorna patrociandores com valores acima da media 
async def get_patrocinadores_com_valores_acima_da_media(db: AsyncSession):
    query = text("""
        SELECT p.id, p.nome, p.email, p.tipo, p.orgao_responsavel, p.responsavel_comercial, p.telefone, p.nome_responsavel
        FROM patrocinadores p
        WHERE NOT EXISTS (
            SELECT 1
            FROM patrocinios pt
            WHERE pt.patrocinador_id = p.id
            AND pt.valor <= ALL (
                SELECT AVG(pt2.valor)
                FROM patrocinios pt2
                GROUP BY pt2.patrocinador_id
            )
        )
    """)
    result = await db.execute(query)
    patrocinadores = result.fetchall()

    return patrocinadores


# notificação pra patrocinadores do tipo privado 
async def criar_gatilho_notificacao_patrocinador_privado(db: AsyncSession):
    try:
        await db.execute(text("DROP TRIGGER IF EXISTS trg_notificacao_patrocinador_privado ON patrocinadores;"))
        query_function = text("""
            CREATE OR REPLACE FUNCTION inserir_log_novo_patrocinador()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.tipo = 'privado' THEN
                    INSERT INTO logs (mensagem, data_criacao, event_details)
                    VALUES (
                        'Novo patrocinador privado: ' || NEW.nome || ' (ID: ' || NEW.id || ')',  -- mensagem
                        CURRENT_TIMESTAMP,                                                      -- data_criacao
                        'Detalhes do evento não disponíveis'                                     -- event_details
                    );
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        await db.execute(query_function)

        query_trigger = text("""
            CREATE TRIGGER trg_notificacao_patrocinador_privado
            AFTER INSERT ON patrocinadores
            FOR EACH ROW
            EXECUTE FUNCTION inserir_log_novo_patrocinador();
        """)
        await db.execute(query_trigger)
        await db.commit()

    except Exception as e:
        await db.rollback()  
        raise e


