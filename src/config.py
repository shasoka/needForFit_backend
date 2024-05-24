import os

from dotenv import load_dotenv

load_dotenv()

# Константы конфигурации для соединения с БД
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# Константы конфигурации для таблиц
TYPES_PRESET = 6  # workout_types

# Константы конфигурации для авторизации
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALG = os.environ.get("JWT_ALG")
TOKEN_EXPIRATION = int(os.environ.get("TOKEN_EXPIRATION"))

# Константы конфигурации для доступа к статичным файлам сервера
SERVER_HOST = os.environ.get("SERVER_HOST")
SERVER_PORT = os.environ.get("SERVER_PORT")
