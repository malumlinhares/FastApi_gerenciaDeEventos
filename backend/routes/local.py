from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.database import get_db
from backend.schemas.local import LocalCreate, LocalResponse
from backend.crud.local import create_local, get_local, update_local, delete_local

router = APIRouter()

@router.post("/", response_model=LocalResponse)
async def create_local_api(local: LocalCreate, db: AsyncSession = Depends(get_db)):
    return await create_local(db=db, local=local)

@router.get("/{local_id}", response_model=LocalResponse)
async def read_local_api(local_id: int, db: AsyncSession = Depends(get_db)):
    db_local = await get_local(db=db, local_id=local_id)
    if db_local is None:
        raise HTTPException(status_code=404, detail="Público não encontrado")
    return db_local


@router.put("/{local_id}", response_model=LocalResponse)
async def update_local_api(
    local_id: int, 
    local: LocalCreate, 
    db: AsyncSession = Depends(get_db)
):
    db_local = await update_local(db=db, local_id=local_id, local=local)
    if db_local is None:
        raise HTTPException (status_code=404, detail = "local nao encontrado")
    return db_local

@router.delete("/{local_id}", response_model=LocalResponse)
async def delete_local_api(
    local_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_local = await delete_local(db=db, local_id=local_id)
    
    if db_local is None:
        raise HTTPException(status_code=404, detail="local não encontrado")
    
    return db_local
