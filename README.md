# Butler

A Python backend service built with FastAPI, featuring AI service integrations, authentication, and modern development practices.

## Quick Start with Template

This project is a template! Generate your own project:

```bash
# Generate a new project
python generate_project.py my-awesome-api

# Or generate in a specific directory
python generate_project.py /path/to/my-project
```

The generator will ask for:
- Project name (lowercase, no spaces)
- Project title/display name
- Description
- Author information
- GitHub repository

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **AI Integration** - Support for OpenAI, Anthropic, and Google AI
- **Authentication** - JWT-based authentication system
- **Database** - PostgreSQL with SQLAlchemy ORM
- **Background Tasks** - Celery with Redis
- **Logging** - Structured logging with rich console output
- **Testing** - Comprehensive test suite with pytest
- **Development Tools** - Pre-commit hooks, linting, and formatting
- **Documentation** - Auto-generated API docs

## Quick Start (for Butler project)

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- PostgreSQL (for production)
- Redis (for background tasks)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd butler
   ```

2. **Install dependencies:**
   ```bash
   make install-dev
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the development server:**
   ```bash
   make dev
   ```

The API will be available at http://localhost:8000

## Development Setup

### Using Make (Recommended)

```bash
# Install dependencies
make install-dev

# Start development server
make dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Run linting
make lint

# Format code
make format

# Run security checks
make security

# Clean build artifacts
make clean
```

### Manual Setup

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-extras --dev

# Activate virtual environment
source .venv/bin/activate

# Install pre-commit hooks
pre-commit install

# Start development server
uvicorn butler.main:app --reload --host 127.0.0.1 --port 8000
```

## Template Usage

### Generating a New Project

```bash
# Run the generator
python generate_project.py

# Follow the prompts to configure your project
Project name (lowercase, no spaces): my-api
Project title [My-Api]: My Awesome API
Project description: An amazing API service
Author name: Your Name
Author email: you@example.com
GitHub repo [your-name/my-api]: yourorg/my-api

# The generator will create a new project with all references updated
```

### What Gets Templatized

The generator replaces these template variables:
- `butler` → your project name
- `Butler` → your project title
- `A Python backend service` → your description
- `Butler Team` → your author name
- `team@butler.dev` → your email
- `butler-team/butler` → your GitHub repo
- Database names and users
- All imports and references

### Template Variables

The template uses these key variables (defined in `template_config.json`):
- `project_name`: Lowercase project name
- `project_name_title`: Display title
- `project_description`: Project description
- `author_name`: Author/team name
- `author_email`: Contact email
- `github_repo`: GitHub repository
- `database_name`: Database name
- `database_user`: Database user

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Application Settings
APP_NAME=Butler
DEBUG=false
HOST=127.0.0.1
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/butler

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services (optional)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_AI_API_KEY=your-google-ai-key
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Project Structure

```
butler/                     # Your project name will replace 'butler'
├── src/butler/            # Main application code
│   ├── api/              # API routes and endpoints
│   │   └── endpoints/    # Individual endpoint modules
│   ├── core/             # Core functionality (config, logging)
│   ├── models/           # Data models
│   ├── services/         # Business logic services
│   └── utils/            # Utility functions
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── scripts/             # Utility scripts
├── nginx/               # Nginx configuration
├── docs/                # Documentation
├── pyproject.toml       # Project configuration
├── Makefile            # Development commands
├── generate_project.py  # Template generator
└── template_config.json # Template configuration
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
uv run pytest tests/unit/test_auth.py -v

# Run integration tests only
uv run pytest tests/integration/ -v

# Run tests with specific markers
uv run pytest -m "unit" -v
```

### Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test complete workflows and API interactions

## Development Workflow

1. **Create a feature branch**
2. **Make your changes**
3. **Run tests**: `make test`
4. **Run linting**: `make lint`
5. **Format code**: `make format`
6. **Commit changes** (pre-commit hooks will run automatically)
7. **Push and create PR**

## API Usage Examples

### Authentication

```bash
# Register a new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### AI Chat

```bash
# Chat with AI (requires authentication token)
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how can you help me?",
    "provider": "openai"
  }'
```

## Production Deployment

### Environment Setup

1. Set up PostgreSQL database
2. Set up Redis instance
3. Configure environment variables
4. Set up reverse proxy (Nginx)
5. Configure SSL certificates
6. Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `make test`
5. Run linting: `make lint`
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Template Maintenance

### Adding New Template Variables

1. Update `template_config.json` with new variables
2. Update `generate_project.py` to handle the new variables
3. Update files that should use the template variables
4. Test the generator with different configurations

### Template Best Practices

- Keep hardcoded project names to a minimum
- Use descriptive template variable names
- Test the generator thoroughly
- Document all template variables
- Maintain backward compatibility when possible

## Support

For questions and support:
- Create an issue on GitHub
- Check the documentation at `/docs`
- Review the API documentation at `/docs` when running