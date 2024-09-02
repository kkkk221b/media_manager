from sqlalchemy.orm import Session
from .models import models, schemas


def create_file(db: Session, file: schemas.FileCreate, uid: str) -> models.FileMetadata:
    db_file = models.FileMetadata(
        uid=uid,
        filename=file.filename,
        filesize=file.filesize,
        fileformat=file.fileformat,
        original_name=file.original_name,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_file_by_uid(db: Session, uid: str) -> models.FileMetadata:
    return db.query(models.FileMetadata).filter(models.FileMetadata.uid == uid).first()


def get_files(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.FileMetadata).offset(skip).limit(limit).all()

