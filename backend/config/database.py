# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncio

DATABASE_URL = "postgresql+asyncpg://admin:123456@localhost/ProjetoDB"

# Usando create_async_engine para sessões assíncronas
engine = create_async_engine(DATABASE_URL, echo=True, future=True, pool_size=20, max_overflow=0, pool_timeout=30)

# Sessão assíncrona
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as db:
        yield db