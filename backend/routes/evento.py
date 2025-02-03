from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.evento import EventoCreate, EventoResponse
from backend.crud.evento import create_evento, get_evento, update_evento, delete_evento

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
