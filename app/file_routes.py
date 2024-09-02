import os

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import uuid

from . import crud
from .helpers import get_files_directory
from .models import models, schemas

from .db import SessionLocal, engine

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload/", response_model=schemas.File)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    uid = str(uuid.uuid4())
    file_directory = get_files_directory()
    file_path = os.path.join(file_directory, f"{uid}_{file.filename}")

    os.makedirs(file_directory, exist_ok=True)

    try:
        # Сохраняем файл на диск
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Вычисляем размер файла
        file.file.seek(0, 2)
        filesize = file.file.tell()
        file.file.seek(0)

        file_metadata = schemas.FileCreate(
            filename=file.filename,
            filesize=filesize,
            fileformat=file.filename.split('.')[-1],
            original_name=file.filename,
        )

        db_file = crud.create_file(db=db, file=file_metadata, uid=uid)
        return db_file
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.get("/files/{uid}", response_model=schemas.File)
def get_file(uid: str, db: Session = Depends(get_db)):
    db_file = crud.get_file_by_uid(db, uid=uid)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

