# main.py
from __future__ import annotations

from fastapi import Depends
from fastapi import FastAPI
from statikk.interfaces.api.controllers.user_controller import get_user_service
from statikk.interfaces.api.controllers.user_controller import user_router

# Initialize the FastAPI application
app = FastAPI()

# Initialize the database client and repository


# Include the user_router from user_controller
app.include_router(user_router, dependencies=[Depends(get_user_service)])
