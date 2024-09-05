from __future__ import annotations

from typing import Dict
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from statikk.core.application.services.collection_service import CollectionService

# Initialize the APIRouter for collections
router = APIRouter()

# Pydantic models for request and response bodies


class CollectionRequest(BaseModel):
    name: str
    schema: dict[str, str]


class CollectionResponse(BaseModel):
    collection_id: str
    name: str
    schema: dict[str, str]


@router.post('/collections', response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
async def create_collection(request: CollectionRequest, service: CollectionService = Depends()):
    """
    Create a new collection.

    :param request: The request body containing the collection's name and schema.
    :type request: CollectionRequest
    :param service: The service used to handle collection-related operations.
    :type service: CollectionService
    :return: The created collection details.
    :rtype: CollectionResponse
    """
    try:
        collection = service.create_collection(name=request.name, schema=request.schema)
        return CollectionResponse(
            collection_id=str(collection.collection_id),
            name=collection.name,
            schema=collection.schema,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/collections/{collection_id}', response_model=CollectionResponse)
async def get_collection(collection_id: str, service: CollectionService = Depends()):
    """
    Retrieve a collection by its unique identifier.

    :param collection_id: The unique ID of the collection.
    :type collection_id: str
    :param service: The service used to handle collection-related operations.
    :type service: CollectionService
    :return: The collection details.
    :rtype: CollectionResponse
    :raises HTTPException: If the collection does not exist.
    """
    try:
        collection = service.get_collection(collection_id)
        return CollectionResponse(
            collection_id=str(collection.collection_id),
            name=collection.name,
            schema=collection.schema,
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/collections/{collection_id}', response_model=CollectionResponse)
async def update_collection(collection_id: str, request: CollectionRequest, service: CollectionService = Depends()):
    """
    Update an existing collection.

    :param collection_id: The unique ID of the collection.
    :type collection_id: str
    :param request: The request body containing the new collection's name and schema.
    :type request: CollectionRequest
    :param service: The service used to handle collection-related operations.
    :type service: CollectionService
    :return: The updated collection details.
    :rtype: CollectionResponse
    :raises HTTPException: If the collection does not exist.
    """
    try:
        updated_collection = service.update_collection(collection_id, name=request.name, schema=request.schema)
        return CollectionResponse(
            collection_id=str(updated_collection.collection_id),
            name=updated_collection.name,
            schema=updated_collection.schema,
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/collections/{collection_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(collection_id: str, service: CollectionService = Depends()):
    """
    Delete a collection by its unique identifier.

    :param collection_id: The unique ID of the collection to delete.
    :type collection_id: str
    :param service: The service used to handle collection-related operations.
    :type service: CollectionService
    :raises HTTPException: If the collection does not exist.
    """
    try:
        service.delete_collection(collection_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/collections', response_model=list[CollectionResponse])
async def list_collections(service: CollectionService = Depends()):
    """
    List all collections.

    :param service: The service used to handle collection-related operations.
    :type service: CollectionService
    :return: A list of all collections.
    :rtype: List[CollectionResponse]
    """
    try:
        collections = service.list_all_collections()
        return [
            CollectionResponse(
                collection_id=str(c.collection_id),
                name=c.name,
                schema=c.schema,
            ) for c in collections
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
