.PHONY: help setup install dev backend frontend \
        db db-down db-reset \
        migrate makemigrations shell \
        lint lint-backend lint-frontend \
        format format-backend format-frontend \
        test test-backend test-frontend \
        full full-down

.DEFAULT_GOAL := help


help:
	@echo "  make setup             Set up the project for local development"
	@echo "  make install           Install backend and frontend dependencies"
	@echo "  make dev               Start PostgreSQL, Django, and Vue"
	@echo "  make db                Start PostgreSQL"
	@echo "  make db-down           Stop PostgreSQL"
	@echo "  make db-reset          Reset PostgreSQL and its data"
	@echo "  make migrate           Run Django database migrations"
	@echo "  make makemigrations    Create new Django migrations"
	@echo "  make shell             Open the Django shell"
	@echo "  make lint              Run all linters"
	@echo "  make format            Format all backend and frontend code"
	@echo "  make test              Run all tests"
	@echo "  make lint-backend      Run Ruff on the backend"
	@echo "  make lint-frontend     Run ESLint on the frontend"
	@echo "  make format-backend    Format backend with Ruff"
	@echo "  make format-frontend   Format frontend with Prettier"
	@echo "  make test-backend      Run pytest"
	@echo "  make full              Run the complete application in Docker"
	@echo "  make full-down         Stop the Docker development environment"


# Set up the project for local development.
setup:
	@echo "Setting up the project..."
	docker compose up -d db
	$(MAKE) install
	$(MAKE) migrate
	@echo "Setup complete."
	@echo "Run 'make dev' to start the development servers."


# Install backend and frontend dependencies.
install:
	@echo "Installing dependencies..."
	cd backend && uv sync
	cd frontend && npm install
	@echo "Dependencies installed."


# Start PostgreSQL, Django, and Vue for local development.
dev: db
	$(MAKE) -j2 backend frontend


# Start the Django development server.
backend:
	@echo "Starting Django..."
	cd backend && uv run python manage.py runserver


# Start the Vue development server.
frontend:
	@echo "Starting Vue..."
	cd frontend && npm run dev


# Start the PostgreSQL database.
db:
	@echo "Starting PostgreSQL..."
	docker compose up -d db


# Stop the PostgreSQL database.
db-down:
	@echo "Stopping PostgreSQL..."
	docker compose stop db


# Delete PostgreSQL data and create a fresh database.
db-reset:
	@echo "Resetting PostgreSQL..."
	docker compose down -v
	docker compose up -d db


# Apply pending Django database migrations.
migrate:
	cd backend && uv run python manage.py migrate


# Create new Django migration files.
makemigrations:
	cd backend && uv run python manage.py makemigrations


# Open the Django interactive shell.
shell:
	cd backend && uv run python manage.py shell


# Run all linters.
lint: lint-backend lint-frontend


# Run Ruff on the Django backend.
lint-backend:
	cd backend && uv run ruff check .


# Run ESLint on the Vue frontend.
lint-frontend:
	cd frontend && npm run lint


# Format all backend and frontend code.
format: format-backend format-frontend


# Format Python code with Ruff.
format-backend:
	cd backend && uv run ruff format .


# Format Vue/JavaScript code with Prettier.
format-frontend:
	cd frontend && npm run format


# Run all tests.
test: test-backend


# Run the Django/Python test suite with pytest.
test-backend:
	cd backend && uv run pytest


# -------------------------
# Docker
# -------------------------

# Run the complete application using Docker.
full:
	docker compose --profile full up --build


# Stop the complete Docker development environment.
full-down:
	docker compose --profile full down

prod:
	docker compose -f docker-compose.prod.yaml up --build