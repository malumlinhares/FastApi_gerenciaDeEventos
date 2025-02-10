from sqlalchemy import text, inspect
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

# Configuração do banco de dados
DATABASE_URL = "postgresql+asyncpg://admin:123456@localhost/EventsDB"
engine = create_async_engine(DATABASE_URL, echo=True)

# Função para excluir todas as tabelas
async def drop_tables():
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

# Executa a função
asyncio.run(drop_tables())
