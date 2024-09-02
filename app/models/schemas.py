import datetime

from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    filename: str
    filesize: int
    fileformat: str
    original_name: str

class FileCreate(FileBase):
    pass

class File(FileBase):
    id: int
    uid: str
    created_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # Разрешаем произвольные типы
    )
