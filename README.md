# fastapi-service

A FastAPI service with PostgreSQL, Alembic migrations, and async database access via asyncpg.

## Requirements

- [Docker](https://www.docker.com/)
- [uv](https://docs.astral.sh/uv/)

## Getting started

### 1. Install dependencies

```bash
uv sync
```

### 2. Set up environment variables

Copy the example and adjust values if needed:

```bash
cp .env.example .env
```

The default `.env` values work out of the box with the provided `docker-compose.yml`.

### 3. Start the local database

```bash
make database-local-start
```

### 4. Run migrations

```bash
make database-local-migrate
```

### 5. Start the application

```bash
make app-start
```

The API will be available at `http://localhost:8000`.  
Interactive docs at `http://localhost:8000/docs`.

---

## Running tests

### Set up the test database

```bash
make database-test-start
make database-test-migrate
```

### Run all tests

```bash
make test
```

### Run only unit or integration tests

```bash
make test-unit
make test-integration
```

---

## Database management (PgAdmin)

```bash
make pgadmin-start
```

Open `http://localhost:5050` and connect with:

| Field    | Value                      |
|----------|----------------------------|
| Host     | `fastapi-service-local-db` |
| Port     | `5432`                     |
| Database | `fastapi_service_db`       |
| Username | `user_admin`               |
| Password | `pass_admin`               |

---

## Migrations

Create a new migration:

```bash
make migration-create name=your_migration_name
```

---

## Linting & formatting

```bash
make lint          # Check for errors
make lint-fix      # Auto-fix errors
make format-fix    # Format code
make format-check  # Check formatting without modifying files
```

---

## All available commands

```bash
make help
```
