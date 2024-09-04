# main.py
from __future__ import annotations

from fastapi import Depends
from fastapi import FastAPI
from statikk.core.application.services.cloud_function_service import CloudFunctionService
from statikk.core.application.services.collection_service import CollectionService
from statikk.core.domain.repositories.collection_repository_impl import SubrrealDBCollectionRepository
from statikk.infrastructure.databases.subrreal_db_client import SubrrealDBClient
from statikk.interfaces.api.controllers.user_controller import get_user_service
from statikk.interfaces.api.controllers.user_controller import user_router

# Initialize the FastAPI application
app = FastAPI()

# Initialize the database client
db_client = SubrrealDBClient(host='localhost', port=1234, database='statikk_db')


# Include the user_router from user_controller
app.include_router(user_router, dependencies=[Depends(get_user_service)])


# Initialize the FastAPI application
app = FastAPI()


# Health check endpoint
@app.get('/')
async def root():
    return {'message': 'Statikk API is running'}
