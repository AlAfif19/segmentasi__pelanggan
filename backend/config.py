import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class Config:
    APP_NAME = os.getenv("APP_NAME", "Sistem Segmentasi Pelanggan")
    APP_DEBUG = os.getenv("APP_DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_key")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "segmentasi_pelanggan")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_ENABLED = os.getenv("DB_ENABLED", "True").lower() == "true"

    EXPORT_CSV_PATH = os.getenv("EXPORT_CSV_PATH", "exports/csv/")
    EXPORT_EXCEL_PATH = os.getenv("EXPORT_EXCEL_PATH", "exports/excel/")
    EXPORT_JSON_PATH = os.getenv("EXPORT_JSON_PATH", "exports/json/")
