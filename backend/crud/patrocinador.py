from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.patrocinador import Patrocinador, TipoPatrocinador
from backend.schemas.patrocinador import PatrocinadorCreate
from sqlalchemy.future import select
from sqlalchemy import text

# Função para criar patrocinador
# async def create_patrocinador(db: AsyncSession, patrocinador: PatrocinadorCreate):
#     db_patrocinador = Patrocinador(
#         nome=patrocinador.nome,
#         email=patrocinador.email,
#         tipo=TipoPatrocinador(patrocinador.tipo),  # Convertendo para o tipo Enum
#         orgao_responsavel=patrocinador.orgao_responsavel,
#         responsavel_comercial=patrocinador.responsavel_comercial,
#     )
#     db.add(db_patrocinador)
#     await db.commit()
#     await db.refresh(db_patrocinador)
#     return db_patrocinador

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


# Função para buscar patrocinadores por substring no nome
# async def search_patrocinador_by_name(db: AsyncSession, nome_substring: str):
#     result = await db.execute(
#         select(Patrocinador).filter(Patrocinador.nome.ilike(f"%{nome_substring}%"))
#     )
#     patrocinadores = result.scalars().all()
#     return patrocinadores

async def search_patrocinador_by_name(db: AsyncSession, nome_substring: str):
    query = text("""
        SELECT * 
        FROM patrocinadores
        WHERE nome ILIKE :nome_substring
    """)
    result = await db.execute(query, {"nome_substring": f"%{nome_substring}%"})
    patrocinadores = result.fetchall()
    return patrocinadores

async def get_patrocinadores_com_valores_acima_da_media(db: AsyncSession):
    """
    Retorna todos os patrocinadores que têm patrocínios com valor superior à média dos seus próprios patrocínios.
    """
    query = text("""
    SELECT p.id, p.nome, p.email, p.tipo
    FROM patrocinadores p
    WHERE p.id = ANY (
        SELECT pt.patrocinador_id
        FROM patrocinios pt
        JOIN eventos e ON e.id = pt.evento_id
        WHERE pt.valor > (
            SELECT AVG(pt2.valor)
            FROM patrocinios pt2
            WHERE pt2.patrocinador_id = pt.patrocinador_id
        )
    )
""")

    result = await db.execute(query)
    patrocinadores = result.fetchall()
    return patrocinadores


async def criar_gatilho_notificacao_patrocinador_privado(db: AsyncSession):
    """
    Cria um gatilho para notificar sobre a inserção de patrocinadores do tipo 'privado'.
    """
    query = text("""
        DO $$ 
        BEGIN
            -- Criar a função apenas se ainda não existir
            IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'notificacao_patrocinador_privado') THEN
                CREATE FUNCTION notificacao_patrocinador_privado()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF NEW.tipo = 'privado' THEN
                        INSERT INTO logs (mensagem, data_criacao)
                        VALUES ('Novo patrocinador privado inserido (ID: ' || NEW.id || '): ' || NEW.nome, CURRENT_TIMESTAMP);
                    END IF;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            END IF;

            -- Remover o gatilho caso já exista para evitar erro
            IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_notificacao_patrocinador_privado') THEN
                DROP TRIGGER trg_notificacao_patrocinador_privado ON patrocinadores;
            END IF;

            -- Criar o gatilho novamente
            CREATE TRIGGER trg_notificacao_patrocinador_privado
            AFTER INSERT ON patrocinadores
            FOR EACH ROW
            EXECUTE FUNCTION notificacao_patrocinador_privado();
        END $$;
    """)

    await db.execute(query)
    await db.commit()
