from dotenv import load_dotenv
import os

load_dotenv()

TESTING = os.getenv("TESTING")
DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
LOCAL_DISK_PATH = os.getenv("LOCAL_DISK_PATH")
GOOGLE_STORE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")