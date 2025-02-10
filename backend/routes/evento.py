from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.config.database import get_db
from backend.schemas.evento import (
    EventoCreate,
    EventoResponse
)

from backend.crud.evento import (
    create_evento, get_evento, update_evento, delete_evento,
    bulk_create_evento, get_eventos_com_patrocinios
)

router = APIRouter()

@router.post("/", response_model=EventoResponse)
async def create_evento_api(evento: EventoCreate, db: AsyncSession = Depends(get_db)):
    return await create_evento(db=db, evento=evento)

@router.get("/{evento_id}", response_model=EventoResponse)
async def read_evento_api(evento_id: int, db: AsyncSession = Depends(get_db)):
    db_evento = await get_evento(db=db, evento_id=evento_id)
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Público não encontrado")
    return db_evento


@router.put("/{evento_id}", response_model=EventoResponse)
async def update_evento_api(
    evento_id: int, 
    evento: EventoCreate, 
    db: AsyncSession = Depends(get_db)
):
    db_evento = await update_evento(db=db, evento_id=evento_id, evento=evento)
    if db_evento is None:
        raise HTTPException (status_code=404, detail = "evento nao encontrado")
    return db_evento

@router.delete("/{evento_id}", response_model=EventoResponse)
async def delete_evento_api(
    evento_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_evento = await delete_evento(db=db, evento_id=evento_id)
    
    if db_evento is None:
        raise HTTPException(status_code=404, detail="evento não encontrado")
    
    return db_evento


# Operações em massa
@router.post("/bulk", response_model=List[EventoResponse])
async def bulk_create_eventos(
    eventos: List[EventoCreate], 
    db: AsyncSession = Depends(get_db)
):
    try:
        return await bulk_create_evento(db, eventos)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/eventos/com-patrocinios", response_model=List[EventoResponse])
async def read_eventos_com_patrocinios(db: AsyncSession = Depends(get_db)):
    """
    Retorna os eventos com a quantidade e o valor total dos patrocínios, 
    filtrando para incluir apenas eventos com mais de 3 patrocínios.
    """
    return await get_eventos_com_patrocinios(db)
