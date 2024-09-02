
# Media Manager

Media Manager — это приложение на базе FastAPI, которое позволяет загружать, хранить и управлять файлами с использованием базы данных и Google Cloud Storage (GCS). 

## Основные возможности

- **Загрузка файлов:** Загружайте файлы на локальный диск и отправляйте их в Google Cloud Storage.
- **Получение файлов:** Загружайте файлы из локального хранилища по их уникальному идентификатору.
- **Удаление файлов:** Удаляйте файлы из базы данных и локального хранилища.

## Структура проекта

```
media_manager/
├── app/                        # Основная логика приложения
│   ├── crud.py                 # Операции с базой данных
│   ├── db.py                   # Настройка базы данных
│   ├── file_routes.py          # Маршруты для работы с файлами
│   ├── models/                 # Модели и схемы данных
│   ├── services/               # Бизнес-логика и вспомогательные функции
│   └── main.py                 # Точка входа в приложение
├── config/                     # Конфигурационные файлы
│   ├── config.py               # Основные настройки приложения
│   └── credentials/            # Учетные данные для Google Cloud
│
├── tests/                      # Тесты
│   └── test_app.py             # Базовые тесты проверки функционала
├── local_disk/                 # Локальное хранилище файлов
├── Dockerfile                  # Dockerfile для создания образа приложения
├── docker-compose.yaml         # Конфигурация для запуска с Docker Compose
├── Makefile                    # Makefile для упрощения задач
└── README.md                   # Текущий файл README
```

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/kkkk221b/media_manager.git
cd media_manager
```

### 2. Настройка окружения

Создайте файл `.env` в корне проекта и добавьте следующие переменные окружения:

```env
DEBUG_MODE=true # режим отладки в приложении.
TESTING=true # приложение запускается тестовом режиме.
DATABASE_URL=postgresql://kk221b:12345@db:5432/files_db # основное бд
TEST_DATABASE_URL=postgresql://kk221b:12345@localhost:5432/files_db_test # тестовое бд
GOOGLE_APPLICATION_CREDENTIALS=service-account-file.json # путь до учетных данных
GCS_BUCKET_NAME=your-gcs-bucket-name # имя бакета в google storage
LOCAL_DISK_PATH=/path/to/local_disk/files # путь до локального диска
```

### 3. Запуск с использованием Docker

```bash
docker-compose up --build
```

Приложение будет доступно по адресу `http://localhost:8000`.

### 4. Использование Makefile

Вы можете использовать `Makefile` для выполнения частых задач, таких как очистка старых файлов:

```bash
make clean_old_files
make setup_cron
```

### 5. Запуск тестов

Для запуска тестов:
```bash
pytest
```


## Использование API

### Загрузка файла

- **Endpoint:** `POST /upload/`
- **Описание:** Загружает файл на сервер и сохраняет его в базе данных и GCS.

### Скачивание файла

- **Endpoint:** `GET /download/{uid}`
- **Описание:** Возвращает файл по его уникальному идентификатору.
