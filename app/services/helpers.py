import os
from google.cloud import storage
from config import config


def get_files_directory():
    return os.path.join(os.getcwd(), config.LOCAL_DISK_PATH)


def create_directories():
    os.makedirs(get_files_directory(), exist_ok=True)


# проверка доступных бакетов
def list_buckets():
    storage_client = storage.Client()
    buckets = list(storage_client.list_buckets())

    print("Buckets in your project:")
    for bucket in buckets:
        print(bucket.name)
