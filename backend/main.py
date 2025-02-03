from fastapi import FastAPI
from backend.config.database import create_tables
from backend.routes import patrocinador, organizador, local, evento, patrocinio
from backend.routes import patrocinio, autenticador, certificado, endereco, inscricao, participante, privilegio_vip,  privilegio

app = FastAPI(title="Minha API FastAPI", description="Gerencia Público e Patrocinadores", version="1.0.0")

@app.on_event("startup")
async def startup():
    await create_tables()

# Incluindo as rotas organizadas
app.include_router(patrocinador.router, prefix="/patrocinadores", tags=["Patrocinadores"])
app.include_router(organizador.router, prefix="/organizadores", tags=["organizadores"])
app.include_router(local.router, prefix="/locais", tags=["locais"])
app.include_router(evento.router, prefix="/eventos", tags=["eventos"])

app.include_router(patrocinio.router, prefix="/patrocinios", tags=["patrocinios"])

# Incluir os routers na aplicação FastAPI
app.include_router(patrocinio.router, prefix="/patrocinios", tags=["patrocinios"])
app.include_router(autenticador.router, prefix="/autenticadores", tags=["autenticadores"])
app.include_router(certificado.router, prefix="/certificados", tags=["certificados"])
app.include_router(endereco.router, prefix="/enderecos", tags=["enderecos"])
app.include_router(inscricao.router, prefix="/inscricoes", tags=["inscricoes"])
app.include_router(participante.router, prefix="/participantes", tags=["participantes"])
app.include_router(privilegio.router, prefix="/privilegios", tags=["privilegios"])
app.include_router(privilegio_vip.router, prefix="/privilegios_vip", tags=["privilegios_vip"])


@app.get("/")
async def root():
    return {"message": "API está rodando 🚀"}
