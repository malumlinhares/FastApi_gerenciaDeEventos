import os
import sys
from fastapi import FastAPI
from backend.config.database import create_tables, test_connection
from backend.routes import (
    patrocinador, organizador, local, evento, patrocinio,
    autenticador, certificado, endereco, inscricao,
    participante
)
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware


DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123456")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")  # Altere aqui, pode ser "localhost" ou IP do seu computador
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "ProjetoDB")



# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Inicialização do FastAPI
app = FastAPI(
    title="Minha API FastAPI",
    description="Gerencia Público e Patrocinadores",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode ser ["http://localhost:5173"] para mais segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definindo o Lifespan para inicialização e desligamento
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lógica de inicialização e finalização da aplicação"""
    
    # Criar a string DSN para a conexão com o banco de dados
    dsn = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Testa a conexão ao banco de dados
    connection_successful = await test_connection(dsn=dsn)
    
    if connection_successful:
        print("Banco de dados conectado com sucesso!")
    else:
        print("Falha ao conectar com o banco de dados.")
    
    # Criar as tabelas se a conexão for bem-sucedida
    if connection_successful:
        await create_tables()

    yield  # Isso indica que o FastAPI pode começar a aceitar requisições
    
    # Lógica de finalização da aplicação (se necessário)
    print("Finalizando aplicação.")

# Configurando o Lifespan no FastAPI
app.lifespan = lifespan

# Incluindo as rotas organizadas
app.include_router(patrocinador.router, prefix="/patrocinadores", tags=["Patrocinadores"])
app.include_router(organizador.router, prefix="/organizadores", tags=["Organizadores"])
app.include_router(local.router, prefix="/locais", tags=["Locais"])
app.include_router(evento.router, prefix="/eventos", tags=["Eventos"])
app.include_router(patrocinio.router, prefix="/patrocinios", tags=["Patrocínios"])
app.include_router(autenticador.router, prefix="/autenticadores", tags=["Autenticadores"])
app.include_router(certificado.router, prefix="/certificados", tags=["Certificados"])
app.include_router(endereco.router, prefix="/enderecos", tags=["Endereços"])
app.include_router(inscricao.router, prefix="/inscricoes", tags=["Inscrições"])
app.include_router(participante.router, prefix="/participantes", tags=["Participantes"])
# app.include_router(privilegio.router, prefix="/privilegios", tags=["Privilégios"])
# app.include_router(privilegio_vip.router, prefix="/privilegios_vip", tags=["Privilégios VIP"])

@app.get("/")
async def root():
    return {"message": "API está rodando 🚀"}
