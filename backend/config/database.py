from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncio
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.inspection import inspect


load_dotenv()

def get_database_url() -> str:

    user = os.getenv("POSTGRES_USER", "admin")  # Valor padrão é "admin" se a variável não estiver definida
    password = os.getenv("POSTGRES_PASSWORD", "123456")  # Valor padrão é "123456"
    host = os.getenv("DB_HOST", "localhost")  # Valor padrão é "localhost" - 172.29.224.1
    port = os.getenv("DB_PORT", 5432)  # Valor padrão é 5432
    database = os.getenv("POSTGRES_DB", "ProjetoDB")  # Valor padrão é "ProjetoDB"
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

async def drop_tables():
    from backend.models import (  
        Patrocinador, Evento, Organizador, Local, Participante, Autenticador, Certificado, 
        Endereco, Inscricao, Patrocinio, PrivilegioVip, Privilegio
    )

    engine = await get_engine()
    async with engine.begin() as conn:
        # Usando run_sync para realizar a inspeção de forma síncrona
        await conn.run_sync(lambda sync_conn: inspect(sync_conn))  # Realiza a inspeção de forma síncrona
        
        # Obtendo o nome de todas as tabelas no esquema público
        result = await conn.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public';
            """)
        )
        tables = result.fetchall()

        # Excluindo todas as tabelas
        for table in tables:
            table_name = table[0]
            await conn.execute(
                text(f"DROP TABLE IF EXISTS public.{table_name} CASCADE")
            )
            print(f"Tabela '{table_name}' excluída com sucesso!")


# Usando create_async_engine para sessões assíncronas
async def get_engine():
    database_url = get_database_url()
    return create_async_engine(database_url, echo=True, future=True, pool_size=20, max_overflow=0, pool_timeout=30)

# Sessão assíncrona
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=None, class_=AsyncSession)

Base = declarative_base()

# Função para criar as tabelas
async def create_tables():
    from backend.models import (  # Importando os modelos para garantir que as tabelas sejam registradas
        Patrocinador, Evento, Organizador, Local, Participante, Autenticador, Certificado, 
        Endereco, Inscricao, Patrocinio, PrivilegioVip, Privilegio
    )
    
    print("Tabelas registradas no SQLAlchemy:", Base.metadata.tables.keys())  # Verificando quais tabelas foram registradas

    engine = await get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




async def get_db():
    engine = await get_engine()
    async_session = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)
    
    async with async_session() as session:
        yield session


async def test_connection(dsn: str):
    try:
        engine = create_async_engine(dsn, echo=True, future=True, pool_size=20, max_overflow=0, pool_timeout=30)
        
        # Tentando executar uma consulta simples
        async with engine.connect() as conn:
            result = await conn.execute(select(1))
            print("Conexão bem-sucedida!", result.fetchall())
            return True
    except OperationalError as e:
        print("Falha na conexão:", e)
        return False
