import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

from app.db import Base


class FileMetadata(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True, nullable=False)
    filename = Column(String, nullable=False)
    filesize = Column(Integer, nullable=False)
    fileformat = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<FileMetadata(uid={self.uid}, filename={self.filename}, file_format={self.fileformat})>"
