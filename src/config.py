import os

from dotenv import load_dotenv

load_dotenv()

# Константы конфигурации для соединения с БД

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# Константы конфигурации для таблицы workout_types

TYPES_PRESET = 6

JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALG = os.environ.get("JWT_ALG")
