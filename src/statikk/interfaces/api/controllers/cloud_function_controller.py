from __future__ import annotations

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from statikk.core.application.services.cloud_function_service import CloudFunctionService

# Initialize the APIRouter for cloud functions
router = APIRouter()

# Pydantic models for request and response bodies


class CloudFunctionRequest(BaseModel):
    name: str
    code: str
    triggers: list[str]


class CloudFunctionResponse(BaseModel):
    function_id: str
    name: str
    code: str
    triggers: list[str]


@router.post('/cloud_functions', response_model=CloudFunctionResponse, status_code=status.HTTP_201_CREATED)
async def create_cloud_function(request: CloudFunctionRequest, service: CloudFunctionService = Depends()):
    """
    Create a new cloud function.

    :param request: The request body containing the cloud function's name, code, and triggers.
    :type request: CloudFunctionRequest
    :param service: The service used to handle cloud function-related operations.
    :type service: CloudFunctionService
    :return: The created cloud function details.
    :rtype: CloudFunctionResponse
    """
    try:
        cloud_function = service.create_cloud_function(name=request.name, code=request.code, triggers=request.triggers)
        return CloudFunctionResponse(
            function_id=str(cloud_function.function_id),
            name=cloud_function.name,
            code=cloud_function.code,
            triggers=cloud_function.triggers,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/cloud_functions/{function_id}', response_model=CloudFunctionResponse)
async def get_cloud_function(function_id: str, service: CloudFunctionService = Depends()):
    """
    Retrieve a cloud function by its unique identifier.

    :param function_id: The unique ID of the cloud function.
    :type function_id: str
    :param service: The service used to handle cloud function-related operations.
    :type service: CloudFunctionService
    :return: The cloud function details.
    :rtype: CloudFunctionResponse
    :raises HTTPException: If the cloud function does not exist.
    """
    try:
        cloud_function = service.get_cloud_function(function_id)
        return CloudFunctionResponse(
            function_id=str(cloud_function.function_id),
            name=cloud_function.name,
            code=cloud_function.code,
            triggers=cloud_function.triggers,
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cloud function not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/cloud_functions/{function_id}', response_model=CloudFunctionResponse)
async def update_cloud_function(function_id: str, request: CloudFunctionRequest, service: CloudFunctionService = Depends()):
    """
    Update an existing cloud function.

    :param function_id: The unique ID of the cloud function.
    :type function_id: str
    :param request: The request body containing the new cloud function's code and triggers.
    :type request: CloudFunctionRequest
    :param service: The service used to handle cloud function-related operations.
    :type service: CloudFunctionService
    :return: The updated cloud function details.
    :rtype: CloudFunctionResponse
    :raises HTTPException: If the cloud function does not exist.
    """
    try:
        updated_cloud_function = service.update_cloud_function(
            function_id=function_id,
            new_code=request.code,
            triggers=request.triggers,
        )
        return CloudFunctionResponse(
            function_id=str(updated_cloud_function.function_id),
            name=updated_cloud_function.name,
            code=updated_cloud_function.code,
            triggers=updated_cloud_function.triggers,
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cloud function not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/cloud_functions/{function_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cloud_function(function_id: str, service: CloudFunctionService = Depends()):
    """
    Delete a cloud function by its unique identifier.

    :param function_id: The unique ID of the cloud function to delete.
    :type function_id: str
    :param service: The service used to handle cloud function-related operations.
    :type service: CloudFunctionService
    :raises HTTPException: If the cloud function does not exist.
    """
    try:
        service.delete_cloud_function(function_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cloud function not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/cloud_functions', response_model=list[CloudFunctionResponse])
async def list_cloud_functions(service: CloudFunctionService = Depends()):
    """
    List all cloud functions.

    :param service: The service used to handle cloud function-related operations.
    :type service: CloudFunctionService
    :return: A list of all cloud functions.
    :rtype: List[CloudFunctionResponse]
    """
    try:
        cloud_functions = service.list_all_cloud_functions()
        return [
            CloudFunctionResponse(
                function_id=str(cf.function_id),
                name=cf.name,
                code=cf.code,
                triggers=cf.triggers,
            ) for cf in cloud_functions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
