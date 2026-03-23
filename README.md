# fastapi-service

A FastAPI service with PostgreSQL, Alembic migrations, and async database access via asyncpg.

## Table of contents

- [Requirements](#requirements)
- [Getting started](#getting-started)
- [Running tests](#running-tests)
- [Database management (PgAdmin)](#database-management-pgadmin)
- [Migrations](#migrations)
- [Linting & formatting](#linting--formatting)
- [All available commands](#all-available-commands)
- [Exercise](#exercise)
- [Bonus Exercise 1 — API Key protection](#bonus-exercise)
- [Bonus Exercise 2 — GitHub Actions CI](#bonus-exercise-2)
- [Bonus Exercise 3 — Concurrent external API calls with asyncio](#bonus-exercise-3)
- [Bonus Exercise 4 — Add CORS middleware](#bonus-exercise-4)

---

## Requirements

- [Docker](https://www.docker.com/) with Docker Compose v2
- [uv](https://docs.astral.sh/uv/)

### Installing Docker & Docker Compose on Ubuntu

> Skip this step if you already have Docker and Docker Compose installed.

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

### Installing uv on Ubuntu

> Skip this step if you already have uv installed. Run `uv --version` to check.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

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
| login    | `admin@admin.com`          |
| Password | `admin`                    |
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

---

## Exercise

### Add a new domain entity

This project includes a fully working `things` domain as a reference implementation. Your task is to create a new domain entity from scratch following the same architecture.

**Entity: `Item`**

An `Item` represents a product or resource with the following fields:

| Field         | Type      | Required | Description                          |
|---------------|-----------|----------|--------------------------------------|
| `id`          | `UUID`    | yes      | Auto-generated primary key           |
| `name`        | `string`  | yes      | Name of the item (max 255 chars)     |
| `price`       | `float`   | yes      | Price of the item (must be positive) |
| `stock`       | `integer` | yes      | Available units (must be >= 0)       |
| `description` | `string`  | no       | Optional description                 |
| `created_at`  | `timestamp` | yes    | Auto-set on creation                 |

### Requirements

1. **Migration** — Create a new Alembic migration that adds the `items` table with the fields above.

2. **Schemas** — Create Pydantic schemas `ItemCreate`, `ItemRead`, and `ItemUpdate` under `src/items/schemas/items.py`. Add field descriptions and examples.

3. **Repository** — Implement a `ItemsPostgresRepository` under `src/items/stores/items.py` extending `BaseRepository` with the following methods:
   - `get_by_id(id: UUID) -> ItemRead | None`
   - `get_all() -> list[ItemRead]`
   - `create(payload: ItemCreate) -> ItemRead`
   - `update(id: UUID, payload: ItemUpdate) -> ItemRead | None`
   - `delete(id: UUID) -> bool`

4. **Service** — Create an `ItemsService` under `src/items/services/items.py` that delegates to the repository.

5. **Router** — Implement a REST router under `src/items/routers/items.py` with the following endpoints and proper HTTP status codes:

   | Method   | Path          | Description              |
   |----------|---------------|--------------------------|
   | `GET`    | `/items/`     | List all items           |
   | `GET`    | `/items/{id}` | Get an item by ID        |
   | `POST`   | `/items/`     | Create a new item        |
   | `PUT`  | `/items/{id}`   | update an item           |
   | `DELETE` | `/items/{id}` | Delete an item           |

6. **Register the router** — Mount the items router in `src/app.py`.

7. **Unit tests** — Write unit tests under `tests/unit/test_items_repository.py` covering at least:
   - `get_by_id` returns an item
   - `get_by_id` returns `None` when not found
   - `create` returns the created item
   - `delete` returns `True` when deleted
   - `delete` returns `False` when not found

8. **Integration tests** — Write integration tests under `tests/integration/test_items.py` covering all endpoints and their edge cases (e.g. 404 responses).

### Tips

- Follow the exact same folder structure and naming conventions as the `things` domain.
- Run `make lint` and `make format-check` before submitting — your code must pass both.
- Run `make test` to verify all tests pass.
- Document your endpoints and schema fields the same way as in `things`.

---

## Bonus Exercise

### Protect all endpoints with an API key

Add a security layer to the application so that all endpoints require a valid API key to be accessed.

#### Requirements

1. **API key value** — Store the expected API key as a hardcoded constant in a new file `src/auth/api_key.py`:

   ```python
   API_KEY = "super-secret-api-key"
   ```

2. **Dependency** — Create a FastAPI dependency `verify_api_key` in `src/auth/dependencies.py` that:
   - Reads the `X-API-Key` header from the incoming request
   - Raises a `401 Unauthorized` error if the header is missing or the value does not match `API_KEY`

   Use FastAPI's `Security` with `APIKeyHeader` from `fastapi.security`:

   ```python
   from fastapi.security import APIKeyHeader

   api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
   ```

3. **Apply globally** — Register the dependency at the router level in both `things` and `items` routers so that every endpoint is protected without repeating the dependency in each route handler.

4. **Update integration tests** — All existing integration tests must pass the correct `X-API-Key` header. Add at least one test that verifies a request without the header returns `401`.

#### Expected behaviour

| Scenario                          | Response       |
|-----------------------------------|----------------|
| Request with correct API key      | Normal response |
| Request with wrong API key        | `401 Unauthorized` |
| Request without `X-API-Key` header | `401 Unauthorized` |

#### Tips

- The `APIKeyHeader` scheme will automatically show an "Authorize" button in `/docs` so you can test it interactively.
- Keep `API_KEY` hardcoded for this exercise — in a real project it should come from an environment variable.

---

## Bonus Exercise 2

### Create a CI pipeline with GitHub Actions

Add a GitHub Actions workflow that runs automatically when a pull request is opened or updated against any branch.

The pipeline must:
1. Check linting with `ruff`
2. Check formatting with `ruff`
3. Start the test database container
4. Apply migrations to the test database
5. Run unit tests
6. Run integration tests

#### Requirements

Create the file `.github/workflows/ci.yml` with the following structure:

- **Trigger** — Run on `pull_request` events targeting any branch.
- **Runner** — Use `ubuntu-latest`.
- **Python** — Install Python `3.12` and set up `uv` using the official Astral action (`astral-sh/setup-uv`).
- **Docker** — Docker and Docker Compose are already available on GitHub-hosted runners, no installation needed.
- **Steps** (in order):

  | Step | Command |
  |------|---------|
  | Install dependencies | `uv sync` |
  | Check linting | `make lint` |
  | Check formatting | `make format-check` |
  | Start test database | `make database-test-start` |
  | Wait for DB to be healthy | `docker compose ps` or use `sleep` |
  | Run migrations on test DB | `make database-test-migrate` |
  | Run unit tests | `make test-unit` |
  | Run integration tests | `make test-integration` |

- **Environment variables** — The workflow must expose `TEST_DATABASE_URL` so that alembic and the integration tests connect correctly:

  ```yaml
  env:
    TEST_DATABASE_URL: postgresql://user_admin:pass_admin@localhost:5440/fastapi_service_db_test
  ```

#### Tips

- Use `docker compose up -d --wait fastapi-service-local-db-test` instead of a plain `sleep` to wait until the container is healthy before running migrations.
- GitHub Actions already has Docker and Docker Compose v2 pre-installed on `ubuntu-latest` — no need to install them.
- To install `uv`, add this step before running any `uv` command:
  ```yaml
  - uses: astral-sh/setup-uv@v5
  ```
- The workflow file must be placed at exactly `.github/workflows/ci.yml` to be picked up by GitHub.

---

## Bonus Exercise 3

### Concurrent external API calls with asyncio

Add a new endpoint that calls **two different public APIs concurrently** using `asyncio.gather` and returns the combined result in a single response.

#### Endpoint

| Method | Path      | Description                                      |
|--------|-----------|--------------------------------------------------|
| `GET`  | `/info`   | Returns combined data from two public APIs       |

#### Public APIs to use

| API | URL | What it returns |
|-----|-----|-----------------|
| [Open Meteo](https://open-meteo.com/) | `https://api.open-meteo.com/v1/forecast?latitude=40.4168&longitude=-3.7038&current=temperature_2m` | Current temperature in Madrid |
| [Dog CEO](https://dog.ceo/dog-api/) | `https://dog.ceo/api/breeds/image/random` | Random dog image URL |

#### Requirements

1. **HTTP client** — Add `httpx` as a project dependency in `pyproject.toml` (with `httpx[asyncio]` or just `httpx>=0.27.0`). Use an `httpx.AsyncClient` to make the requests.

2. **Response schema** — Create a Pydantic schema `InfoRead` with at least:
   ```python
   class InfoRead(BaseModel):
       temperature_celsius: float
       dog_image_url: str
   ```

3. **Concurrent calls** — Use `asyncio.gather` to fire both HTTP requests at the same time, not sequentially:
   ```python
   import asyncio
   weather_response, dog_response = await asyncio.gather(
       client.get("https://..."),
       client.get("https://..."),
   )
   ```

4. **Router** — Create a new router `src/info/routers/info.py` and register it in `src/app.py`.

5. **Unit test** — Write a unit test that mocks both HTTP calls (use `unittest.mock.AsyncMock` or `pytest-httpx`) and asserts the response schema is correct.

#### Expected response

```json
{
  "temperature_celsius": 18.4,
  "dog_image_url": "https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg"
}
```

#### Tips

- Wrap the `httpx.AsyncClient` in an `async with` block inside the route handler to ensure the connection is properly closed.
- `asyncio.gather` runs both coroutines **concurrently** — the total time is approximately `max(t1, t2)` instead of `t1 + t2`.
- If one of the external APIs is down, the whole `gather` will raise an exception. For extra credit, handle each failure gracefully and return a partial response.

---

## Bonus Exercise 4

### Add CORS middleware

A frontend application is already built and running at `http://localhost:3000`. Without CORS headers, the browser will block any request it makes to this API.

Your task is to configure FastAPI's CORS middleware so the frontend can communicate with the API.

#### Requirements

1. **Add the middleware** — Use `CORSMiddleware` from `starlette.middleware.cors` in `src/app.py`:

   ```python
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=...,
       allow_methods=...,
       allow_headers=...,
   )
   ```

2. **Allowed origins** — Only allow requests from the frontend origin `http://localhost:3000`. Do **not** use `allow_origins=["*"]`.

3. **Allowed methods** — Allow only the HTTP methods actually used by the API: `GET`, `POST`, `POST`, `PATCH`, `DELETE`.

4. **Allowed headers** — Allow the `Content-Type` and `X-API-Key` headers (required for the API key authentication implemented in Bonus Exercise 1).

5. **Configuration via environment variable** — The allowed origin should not be hardcoded. Read it from an environment variable `CORS_ALLOWED_ORIGIN` with `http://localhost:3000` as the default value. Add it to the `Settings` class in `src/config.py` and to the `.env` file.

#### Expected behaviour

| Request origin            | Response                        |
|---------------------------|---------------------------------|
| `http://localhost:3000`   | Includes `Access-Control-Allow-Origin` header |
| `http://evil.com`         | No CORS headers — browser blocks the request  |

#### Tips

- CORS is enforced by the **browser**, not the server. The server always responds — it just includes (or omits) the `Access-Control-Allow-Origin` header. This is why you won't see a difference testing with `curl` or the `/docs` UI.
- The middleware must be registered **before** any routes are included in the app.
- `allow_credentials=True` is only needed if the frontend sends cookies or `Authorization` headers — it is not required here.

