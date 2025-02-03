from sqlalchemy import text, inspect
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

# Configuração do banco de dados
DATABASE_URL = "postgresql+asyncpg://admin:123456@localhost/ProjetoDB"
engine = create_async_engine(DATABASE_URL, echo=True)

# Função para excluir as tabelas
async def drop_tables():
    async with engine.begin() as conn:
        # Usando run_sync para realizar a inspeção de forma síncrona
        await conn.run_sync(lambda sync_conn: inspect(sync_conn))  # Realiza a inspeção de forma síncrona
        
        # Excluindo as tabelas patrocinadores, publicos e privados
        await conn.execute(
            text("""
               UPDATE patrocinadores SET tipo = 'privado' WHERE tipo = 'patrocinador';
;
            """)
        )
        print("Tabelas 'patrocinadores', 'publicos' e 'privados' excluídas com sucesso!")

# Executa a função
asyncio.run(drop_tables())
