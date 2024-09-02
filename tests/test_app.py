import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.app import create_app
from config import config

# Создание тестовой базы данных
DATABASE_URL = config.TEST_DATABASE_URL  # Убедитесь, что у вас есть тестовая база данных

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание приложения для тестирования
app = create_app()


# Заменяем зависимость get_db на сессию с тестовой базой данных
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Фикстура для настройки тестовой базы данных
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_upload_file():
    file_content = b"test file content"
    file_name = "test.txt"
    temp_file_path = os.path.join("test_files", file_name)
    os.makedirs("test_files", exist_ok=True)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)

    with open(temp_file_path, "rb") as temp_file:
        response = client.post("/api/v1/upload/", files={"file": (file_name, temp_file, "text/plain")})

    assert response.status_code == 200
    assert "filename" in response.json()
    assert response.json()["filename"] == file_name

    # Удаление временного файла после теста
    os.remove(temp_file_path)

    # Возвращаем уникальный идентификатор загруженного файла для использования в других тестах
    return response.json()["uid"]


def test_download_file():
    # Загружаем файл и получаем его уникальный идентификатор
    file_content = b"test file content"
    file_name = "test.txt"
    temp_file_path = os.path.join("test_files", file_name)
    os.makedirs("test_files", exist_ok=True)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)

    with open(temp_file_path, "rb") as temp_file:
        upload_response = client.post("/api/v1/upload/", files={"file": (file_name, temp_file, "text/plain")})

    assert upload_response.status_code == 200
    uid = upload_response.json()["uid"]

    # Пытаемся скачать файл по полученному UID
    response = client.get(f"/api/v1/download/{uid}")

    assert response.status_code == 200
    assert response.headers["content-disposition"].startswith("attachment")

    # Удаление временного файла после теста
    os.remove(temp_file_path)
