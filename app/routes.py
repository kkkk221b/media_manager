import os
import uuid
import asyncio

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from starlette.responses import FileResponse

from google.cloud import storage
from google.oauth2 import service_account
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import aiofiles

from config import config
from . import crud
from .models import schemas
from .db import SessionLocal
from app.services.helpers import get_files_directory

router = APIRouter()


# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload/", response_model=schemas.File)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    uid = str(uuid.uuid4())  # Генерация уникального идентификатора для файла
    file_directory = get_files_directory()
    file_path = os.path.join(file_directory, f"{uid}_{file.filename}")

    os.makedirs(file_directory, exist_ok=True)

    try:
        # Асинхронное сохранение файла на диск
        async with aiofiles.open(file_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)

        file_size = os.path.getsize(file_path)

        # Запись метаданных файла в базу данных
        file_metadata = schemas.FileCreate(
            filename=file.filename,
            filesize=file_size,
            fileformat=file.filename.split('.')[-1],
            original_name=file.filename,
        )
        db_file = crud.create_file(db=db, file=file_metadata, uid=uid)

        # Асинхронная отправка файла в Google Cloud Storage
        try:
            credentials = service_account.Credentials.from_service_account_file(config.GOOGLE_STORE_CREDENTIALS)
            storage_client = storage.Client(credentials=credentials)
            bucket = storage_client.bucket(config.GCS_BUCKET_NAME)
            blob = bucket.blob(os.path.basename(file_path))

            def upload_to_gcs():
                with open(file_path, "rb") as f:
                    blob.upload_from_file(f)

            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, upload_to_gcs)

        except Exception as gcs_error:
            # Если не удалось загрузить в GCS, удалить файл из базы данных
            crud.delete_file(db, uid)
            raise HTTPException(status_code=500, detail=f"Failed to upload to GCS: {str(gcs_error)}")

        return db_file

    except (OSError, SQLAlchemyError) as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.get("/download/{uid}", response_class=FileResponse)
async def download_file(uid: str, db: Session = Depends(get_db)):
    # Поиск файла в базе данных по уникальному идентификатору
    db_file = crud.get_file_by_uid(db, uid)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = os.path.join(config.LOCAL_DISK_PATH, f"{uid}_{db_file.filename}")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(path=file_path, filename=db_file.original_name, media_type='application/octet-stream')
