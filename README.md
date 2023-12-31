# Инструкция по развертыванию приложения

### Требования для запуска
1. PostgreSQL >= 15.5
2. Python >= 3.11

### Подготовительный этап
Все описанные ниже операции производятся в терминале из корня проекта.

1. Разворачиваем БД. Для этого:
   ```
   psql -U postgres -h localhost -f .\migrations\migrate.sql -f .\migrations\seed.sql
   ```
   Скрипт ```migrate.sql``` создает БД с именем nff и пятью таблицами. 
   Скрипт ```seed.sql``` заполняет таблицы плейсхолдерами.
2. Создаем файл с именем ```.env```. Его содержимое должно иметь следующую структуру:
   ```
   DB_HOST=<postgresql host>
   DB_PORT=<postgresql port>
   DB_NAME=nff
   DB_USER=<postgesql username>
   DB_PASS=<postgresql password>
   ```
   По дефолту хостом является ```localhost```, а портом - ```5432``` (смотрите ```example.env```)
3. Создаем виртуальное окружение и активируем его:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```
   Самый важный пункт! Обязательно активируйте виртуальное окружение, чтобы иметь доступ к модулю, ответственному за сервер.

4. Устанавливаем зависимости проекта:
   ```
   pip install -r .\requirements.txt
   ```
5. Готовность номер один. Готовы к взлету.

### Запуск сервера
1. Запускаем сервер:
   ```
   python.exe -m uvicorn src.main:app --reload
   ```
2. Вы также можете добавить профиль запуска в вашей IDE. Он должен выглядеть следующим образом:
   ![run_profile](https://github.com/shasoka/needForFit_backend/assets/90062361/fcce8ed6-e659-4287-ab92-f4c623c62800)
3. Победа!
