from fastapi import FastAPI

from app.models import models
from app.services.helpers import create_directories
from app.routes import router as file_router
from app.db import engine
from config import config


def create_app():
    create_directories()
    models.Base.metadata.create_all(bind=engine)
    app = FastAPI(docs_url='/api/docs')
    app.include_router(file_router, prefix="/api/v1", tags=["files"])
    return app
