import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from backend.config.database import Base  # Certifique-se de que Base está sendo importado corretamente
from backend.models.patrocinador import Patrocinador  # Importando os modelos
from backend.models.evento import Evento
from backend.models.organizador import Organizador
from backend.models.local import Local
from backend.models.participante import Participante
from backend.models.autenticador import Autenticador
from backend.models.certificado import Certificado
from backend.models.endereco import Endereco
from backend.models.inscricao import Inscricao
from backend.models.patrocinio import Patrocinio
from sqlalchemy.ext.asyncio import AsyncSession

# Configuração do banco de dados
DATABASE_URL = "postgresql+asyncpg://admin:123456@localhost/ProjetoDB"

# Criando o motor assíncrono e a sessão
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Função assíncrona para criar as tabelas (se não existirem ou se precisarem ser atualizadas)
async def create_tables():
    try:
        async with engine.begin() as conn:
            # Criação de todas as tabelas definidas nos models
            await conn.run_sync(Base.metadata.create_all)
            # await conn.execute("""
            #     CREATE TABLE IF NOT EXISTS logs (
            #         id SERIAL PRIMARY KEY,
            #         mensagem TEXT NOT NULL,
            #         data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            #     );
            # """)
            
            print("Tabelas criadas ou atualizadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar/atualizar as tabelas: {e}")

# Função principal para rodar o código assíncrono
async def run():
    await create_tables()

if __name__ == "__main__":
    asyncio.run(run())  # Aqui a execução do código é assíncrona
