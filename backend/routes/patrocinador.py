from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.patrocinador import PatrocinadorCreate, PatrocinadorResponse
from backend.crud.patrocinador import create_patrocinador, get_patrocinador, delete_patrocinador, update_patrocinador, bulk_create_patrocinador, search_patrocinador_by_name, get_patrocinadores_com_valores_acima_da_media, criar_gatilho_notificacao_patrocinador_privado
from typing import List

router = APIRouter()

@router.post("/", response_model=PatrocinadorResponse)
async def create_patrocinador_api(patrocinador: PatrocinadorCreate, db: AsyncSession = Depends(get_db)):
    print(f"JSON recebido: {patrocinador.dict()}")  # Debug para verificar o JSON
    return await create_patrocinador(db=db, patrocinador=patrocinador)

@router.get("/{patrocinador_id}", response_model=PatrocinadorResponse)
async def read_patrocinador_api(patrocinador_id: int, db: AsyncSession = Depends(get_db)):
    db_patrocinador = await get_patrocinador(db=db, patrocinador_id=patrocinador_id)
    if db_patrocinador is None:
        raise HTTPException(status_code=404, detail="Patrocinador não encontrado")
    return db_patrocinador

@router.put("/{patrocinador_id}", response_model=PatrocinadorResponse)
async def update_patrocinador_api(
    patrocinador_id: int, 
    patrocinador: PatrocinadorCreate, 
    db: AsyncSession = Depends(get_db)
):
    db_patrocinador = await update_patrocinador(db=db, patrocinador_id=patrocinador_id, patrocinador=patrocinador)
    if db_patrocinador is None:
        raise HTTPException (status_code=404, detail = "Patrocinador nao encontrado")
    return db_patrocinador

@router.delete("/{patrocinador_id}", response_model=PatrocinadorResponse)
async def delete_patrocinador_api(
    patrocinador_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_patrocinador = await delete_patrocinador(db=db, patrocinador_id=patrocinador_id)
    
    if db_patrocinador is None:
        raise HTTPException(status_code=404, detail="Patrocinador não encontrado")
    
    return db_patrocinador

@router.post("/bulk", response_model=List[PatrocinadorResponse])
async def bulk_create_patrocinadores(
    patrocinadores: List[PatrocinadorCreate], 
    db: AsyncSession = Depends(get_db)
):
    try:
        return await bulk_create_patrocinador(db, patrocinadores)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Nova rota para buscar patrocinadores por substring no nome
@router.get("/search/", response_model=List[PatrocinadorResponse])
async def search_patrocinador_api(nome_substring: str, db: AsyncSession = Depends(get_db)):

    db_patrocinadores = await search_patrocinador_by_name(db=db, nome_substring=nome_substring)
    if not db_patrocinadores:
        raise HTTPException(status_code=404, detail="Patrocinadores não encontrados")
    return db_patrocinadores

@router.get("/patrocinadores/com-valores-acima-da-media", response_model=List[PatrocinadorResponse])
async def read_patrocinadores_com_valores_acima_da_media(db: AsyncSession = Depends(get_db)):
    """
    Retorna todos os patrocinadores que têm patrocínios com valor superior à média dos seus próprios patrocínios.
    """
    return await get_patrocinadores_com_valores_acima_da_media(db)


@router.post("/gatilho/criar-notificacao-patrocinador-privado")
async def create_gatilho_notificacao_patrocinador_privado(db: AsyncSession = Depends(get_db)):
    """
    Cria um gatilho para notificar sobre a inserção de patrocinadores do tipo 'privado'.
    """
    await criar_gatilho_notificacao_patrocinador_privado(db)
    return {"message": "Gatilho criado com sucesso!"}
