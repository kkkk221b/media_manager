import os

from fastapi import FastAPI

from app.models import models
from app.helpers import create_directories
from app.file_routes import router as file_router
from app.db import engine




def create_app():
    create_directories()
    models.Base.metadata.create_all(bind=engine)
    app = FastAPI(debug=True, docs_url='/api/docs')
    app.include_router(file_router, prefix="/api/v1", tags=["files"])

    return app
