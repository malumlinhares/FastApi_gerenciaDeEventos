import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base  # Certifique-se de que Base está sendo importado corretamente
from models.patrocinador import Patrocinador  # Importando os modelos
from models.evento import Evento
from models.organizador import Organizador
from models.local import Local
from models.participante import Participante
from models.autenticador import Autenticador
from models.certificado import Certificado
from models.endereco import Endereco
from models.inscricao import Inscricao
from models.patrocinio import Patrocinio
from models.privilegio_vip import PrivilegioVip
from models.privilegio import Privilegio
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
            print("Tabelas criadas ou atualizadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar/atualizar as tabelas: {e}")

# Função principal para rodar o código assíncrono
async def run():
    await create_tables()

if __name__ == "__main__":
    asyncio.run(run())  # Aqui a execução do código é assíncrona
