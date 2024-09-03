from fastapi import APIRouter, Depends, HTTPException
from statikk.core.application.services.collection_service import CollectionService
from pydantic import BaseModel
from typing import List

router = APIRouter()

class CollectionResponse(BaseModel):
    collection_id: str
    name: str
    schema: dict

@router.get("/collections", response_model=List[CollectionResponse])
async def list_collections(collection_service: CollectionService = Depends()):
    try:
        collections = collection_service.list_all_collections()
        return [CollectionResponse(collection_id=str(c.collection_id), name=c.name, schema=c.schema) for c in collections]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
