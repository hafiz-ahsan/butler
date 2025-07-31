# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Primary Development Workflow
- `make dev` - Start development server (uses `./scripts/dev.sh`)
- `make test` - Run all tests
- `make test-cov` - Run tests with coverage report
- `make lint` - Run full linting suite (black, isort, flake8, mypy, bandit, safety)
- `make format` - Format code with black and isort

### Testing Commands
- `uv run pytest tests/ -v` - Run all tests with verbose output
- `uv run pytest tests/unit/test_auth.py -v` - Run specific test file
- `uv run pytest tests/integration/ -v` - Run integration tests only
- `uv run pytest -m "unit" -v` - Run tests with specific markers

### Package Management
- `uv sync --all-extras --dev` - Install all dependencies including dev tools
- `uv sync` - Install production dependencies only

## Architecture Overview

This is a **FastAPI-based Python backend service** with the following key architectural components:

### Core Structure
- **FastAPI Application**: Modern async web framework with automatic API documentation
- **Multi-AI Provider Support**: Integrated support for OpenAI, Anthropic, and Google AI services
- **JWT Authentication**: Token-based authentication system with user management
- **PostgreSQL + SQLAlchemy**: Async database operations with ORM
- **Redis + Celery**: Background task processing and caching
- **Structured Logging**: JSON-formatted logging with structlog and rich console output

### Directory Organization
```
src/butler/                 # Main application package
├── api/                   # API layer
│   ├── endpoints/         # Individual endpoint modules (auth, ai, health)
│   └── routes.py         # Route aggregation
├── core/                 # Core functionality
│   ├── config.py         # Settings and configuration management
│   └── logging.py        # Logging configuration
├── models/               # Data models (SQLAlchemy)
├── services/             # Business logic services
│   └── ai_service.py     # AI provider integrations
├── utils/                # Shared utilities
├── main.py               # FastAPI application factory
└── cli.py                # Command-line interface
```

### Key Configuration Patterns
- **Environment-based Configuration**: Uses pydantic-settings with `.env` file support
- **Dependency Injection**: FastAPI's dependency injection for settings, database, etc.
- **Async/Await**: Fully async application using asyncio patterns
- **Middleware Stack**: CORS, trusted host, request logging, and global exception handling

### AI Service Integration
The service provides a unified interface for multiple AI providers:
- OpenAI GPT models
- Anthropic Claude models  
- Google Generative AI models

Authentication is required for AI endpoints, accessed via `/api/v1/ai/chat`.

### Template System
This project serves as a **template** for generating new FastAPI services:
- `generate_project.py` - Template generator script
- `template_config.json` - Template variable definitions
- All project-specific names and identifiers are templatized

### Testing Strategy
- **Unit Tests**: Individual component testing in `tests/unit/`
- **Integration Tests**: Full workflow testing in `tests/integration/`
- **Test Markers**: Use `@pytest.mark.unit` and `@pytest.mark.integration`
- **Async Testing**: Uses `pytest-asyncio` for async test support

## Development Notes

### Code Quality Tools
The project enforces strict code quality with:
- **Black**: Code formatting (88 character line length)
- **isort**: Import sorting with black compatibility
- **Flake8**: Style and complexity checking
- **MyPy**: Static type checking with strict settings
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checking

### Pre-commit Hooks
Pre-commit hooks are automatically installed with `make install-dev` and run all linting tools before commits.

### Database Migrations
When using Alembic for database migrations:
- `make db-migrate` - Apply migrations
- `make db-migration MESSAGE="description"` - Create new migration
- `make db-downgrade` - Rollback one migration

### Environment Variables
Key environment variables in `.env`:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string  
- `SECRET_KEY` - JWT secret key
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_AI_API_KEY` - AI service keys
- `DEBUG` - Enable debug mode and API docs

Always run `make lint` before committing code changes to ensure code quality standards are met.