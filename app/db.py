import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import DATABASE_URL, TEST_DATABASE_URL, TESTING

engine = create_engine(TEST_DATABASE_URL if TESTING else DATABASE_URL)  # движок для подключения к бд
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # сессия для взаимодействия с базой данных
Base = sqlalchemy.orm.declarative_base()  # базовый класс для всех моделей


# Функция для получения сессии базы данных
def get_db():
    """
    Получает сессию базы данных для запроса.

    :return: Генератор, который возвращает сессию базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()