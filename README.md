# Тестовое задание

## Запуск (Docker)

```shell
cp .env.example .env
sudo docker compose up -d --build
```

После запуска приложение будет доступно по адресу:
[http://localhost:8000](http://localhost:8000)

---

## Запуск (на хосте)

### 1. Настройка venv

```shell
python -m venv venv
```

Активация окружения:

```shell
source venv/bin/activate (Linux)
venv\Scripts\activate (Windows)
```

### 2. Установка зависимостей

```shell
pip install -r requirements.txt
```

### 3. Настройка PostgreSQL

```sql
CREATE
DATABASE payments_db;
CREATE
USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE
payments_db TO postgres;
```

для `.env`:

```dotenv
# Postgres
#----------------------
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=payments_db
POSTGRES_HOST=localhost
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/payments_db
```

### 4. Запуск приложения

```shell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

После запуска приложение доступно по адресу:
[http://localhost:8000](http://localhost:8000)
### 5. Генерация signature для транзакции
```shell
(.venv) python scripts/signature_generator.py
```

---

## Тестовые учётные данные

* Пользователь: `user@example.com / userpassword`
* Админ: `admin@example.com / adminpassword`

