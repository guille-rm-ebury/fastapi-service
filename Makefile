.PHONY: database-local-start database-local-migrate database-local-clean \
        database-local-test-start database-local-test-migrate database-local-test-clean \
        pgadmin-start migration-create app-start \
        test test-unit test-integration \
        lint lint-fix format-fix format-check help

help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  Local database:"
	@echo "    database-local-start       Start the local PostgreSQL container"
	@echo "    database-local-migrate     Run migrations against the local database"
	@echo "    database-local-clean       Remove the local database container and volume"
	@echo ""
	@echo "  Test database:"
	@echo "    database-test-start        Start the test PostgreSQL container"
	@echo "    database-test-migrate      Run migrations against the test database"
	@echo "    database-test-clean        Remove the test database container and volume"
	@echo ""
	@echo "  PgAdmin:"
	@echo "    pgadmin-start              Start the PgAdmin container"
	@echo ""
	@echo "  Migrations:"
	@echo "    migration-create name=xxx  Create a new migration with the given name"
	@echo ""
	@echo "  Application:"
	@echo "    app-start                  Start the application locally (hot-reload)"
	@echo ""
	@echo "  Tests:"
	@echo "    test                       Run all tests"
	@echo "    test-unit                  Run unit tests"
	@echo "    test-integration           Run integration tests"
	@echo ""
	@echo "  Linting & formatting:"
	@echo "    lint                       Check for errors with ruff"
	@echo "    lint-fix                   Auto-fix errors with ruff"
	@echo "    format-fix                 Format code with ruff"
	@echo "    format-check               Check formatting without modifying files"
	@echo ""

# --- Local DB ---
database-local-start:
	docker compose up -d fastapi-service-local-db

database-local-migrate:
	uv run alembic upgrade head

database-local-clean:
	docker compose down fastapi-service-local-db -v

# --- Test DB ---
database-test-start:
	docker compose up -d fastapi-service-local-db-test

database-test-migrate:
	DATABASE_URL=postgresql://user_admin:pass_admin@localhost:5440/fastapi_service_db_test \
	uv run alembic upgrade head

database-test-clean:
	docker compose down fastapi-service-local-db-test -v

# --- PgAdmin ---
pgadmin-start:
	docker compose up -d pgadmin

# --- Migrations ---
migration-create:
	uv run alembic revision -m "$(name)"

# --- App ---
app-start:
	uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# --- Tests ---
test:
	uv run --group test pytest tests/

test-unit:
	uv run --group test pytest tests/unit/

test-integration:
	uv run --group test pytest tests/integration/

# --- Linting & Formatting ---
lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

format-fix:
	uv run ruff format .

format-check:
	uv run ruff format --check .
