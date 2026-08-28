# Django Vue Template

A starter template built with Django REST Framework and Vue 3 that provides a solid foundation for building modern web applications.

![Django Vue template](Django_vue_template.png)

## What's included
- Cookie-based JWT authentication using HttpOnly cookies
- Docker development and production environment
- Custom user model with email and username authentication
- User registration and login
- Example task app with CRUD operations
- Standardized API responses
- OpenAPI schema and interactive API documentation
- Light and dark theme

## Features
#### Frontend:

- [Vue 3](https://vuejs.org/): frontend framework with [Vite](https://vite.dev/)
- [Vue Router](https://router.vuejs.org/): routing
- [Pinia](https://pinia.vuejs.org/): state management
- [PrimeVue](https://primevue.org/): UI component library
- [Tailwind CSS](https://tailwindcss.com/): styling
- [Axios](https://axios-http.com/): API client


#### Backend:

- [Django](https://www.djangoproject.com/): web framework
- [Django REST Framework](https://www.django-rest-framework.org/): Django toolkit for building Web APIs
- [PostgreSQL](https://www.postgresql.org/): database
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/): JWT authentication
- [pytest](https://docs.pytest.org/): Python tests with [pytest-django](https://pytest-django.readthedocs.io/en/stable/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/): interactive OpenAPI documentation
  
  
#### Developer Experience:

- [Docker](https://docs.docker.com/): multi-stage builds for development and production
- [ESLint](https://eslint.org/) & [Prettier](https://prettier.io/): frontend linting and formatting
- [Ruff](https://docs.astral.sh/ruff/): backend linting and formatting 
- [pre-commit](https://pre-commit.com/): hooks for frontend and backend checks (optional) 


## Quickstart
This template can be setup and run in three ways:
- Full Docker
- Hybrid
- Native

Before using any setup create the environment:

```bash
cp .env.example .env
```

### Full Docker

Requires [Docker Desktop](https://docs.docker.com/desktop/).

```powershell
docker compose --profile full up --build
docker compose --profile full exec backend python manage.py migrate
```

### Hybrid

Runs PostgreSQL in Docker and Django/Vue locally. Requires Docker Desktop, Python 3.12+, Node.js 22.18+ or 24.12+, and npm.

Start PostgreSQL:

```powershell
docker compose up -d
```

Install and start the backend:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

In another terminal, install and start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

### Native

Runs PostgreSQL, Django, and Vue locally. Requires Python 3.12+, Node.js 22.18+ or 24.12+, npm, and PostgreSQL 17+.

Start the backend after PostgreSQL is running:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

In another terminal, install and start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

## URLs

- Frontend: http://localhost:5173
- API: http://localhost:8000/api/
- API docs: http://localhost:8000/api/docs/
- OpenAPI schema: http://localhost:8000/api/schema/
- Health check: http://localhost:8000/api/health/
- Django admin: http://localhost:8000/admin/


