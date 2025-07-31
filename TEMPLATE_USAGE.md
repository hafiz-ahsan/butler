# Python Backend Service Template

This is a production-ready template for creating Python backend services with FastAPI, AI integrations, authentication, and modern development practices.

## Quick Start

### Generate a New Project

```bash
# Clone this template repository
git clone <template-repo-url>
cd python-backend-template

# Generate your new project
python generate_project.py

# Follow the prompts:
# Project name (lowercase, no spaces): my-awesome-api
# Project title [My-Awesome-Api]: My Awesome API
# Project description: An amazing API for my application
# Author name: Your Name
# Author email: your.email@example.com
# GitHub repo [your-name/my-awesome-api]: yourorg/my-awesome-api
# Target directory [my-awesome-api]:

# Your new project is ready!
cd my-awesome-api
make install-dev
make dev
```

### What You Get

- **FastAPI** backend with modern Python practices
- **AI integrations** (OpenAI, Anthropic, Google AI)
- **JWT authentication** system
- **PostgreSQL** database with SQLAlchemy
- **Redis** for caching and background tasks
- **Comprehensive testing** with pytest (19 tests included)
- **CI/CD** ready with pre-commit hooks
- **Rich CLI** interface
- **Production deployment** configs

## Template Variables

The generator replaces these template variables throughout the codebase:

| Template Variable | Example Value | Description |
|------------------|---------------|-------------|
| `butler` | `my-api` | Lowercase project name (used in imports, configs) |
| `Butler` | `My API` | Project title (used in titles, descriptions) |
| `A Python backend service` | `My amazing API service` | Project description |
| `Butler Team` | `Your Team` | Author/team name |
| `team@butler.dev` | `your@email.com` | Contact email |
| `butler-team/butler` | `yourorg/my-api` | GitHub repository |

## Files That Get Templatized

### Core Configuration
- `pyproject.toml` - Project metadata, dependencies, and build config
- `.env.example` - Environment variables template
- `Makefile` - Development commands

### Source Code
- All Python files in `src/` - Import statements and references
- CLI interface - Help text and commands
- Configuration classes - Default values
- Documentation strings

### Documentation
- `README.md` - Project documentation
- API examples and usage instructions

### Directory Structure
- `src/butler/` → `src/your-project-name/`
- All subdirectories renamed accordingly

## Template Features

### Production Ready
- Comprehensive error handling
- Structured logging with rich output
- Security best practices
- Health check endpoints
- Graceful shutdown handling

### Testing
- Unit tests (13 tests)
- Integration tests (3 tests)
- Test fixtures and utilities
- Coverage reporting (82%+ coverage)
- Mock implementations for AI services

### Development Experience
- Hot reload development server
- Pre-commit hooks for code quality
- Linting and formatting (Black, isort, flake8, mypy)
- Security scanning (Bandit, Safety)
- Rich CLI with helpful commands

### Deployment
- Nginx reverse proxy configuration
- Database initialization scripts
- Environment-based configuration

### AI Integrations
- OpenAI GPT models
- Anthropic Claude
- Google Generative AI
- Unified interface for all providers
- Configurable model parameters

## Customization

### Adding New Template Variables

1. Update `template_config.json`:
   ```json
   {
     "new_variable": "default_value"
   }
   ```

2. Update `generate_project.py` to collect the new variable from user input

3. Use the variable in your template files where needed

### Template Best Practices

- Keep hardcoded values minimal
- Use descriptive variable names
- Test the generator with different inputs
- Document all template variables
- Maintain consistency across files

## Architecture

```
your-project/
├── src/your-project/          # Main application
│   ├── api/                   # API routes and endpoints
│   ├── core/                  # Configuration and logging
│   ├── models/                # Data models
│   ├── services/              # Business logic
│   └── utils/                 # Utilities
├── tests/                     # Test suite
├── Makefile                   # Development commands
└── README.md                  # Project documentation
```

## Example Generated Project

After running the generator with:
- Project name: `weather-api`
- Title: `Weather API`
- Description: `A comprehensive weather data API`

You get:
- Import statements: `from weather_api.core.config import settings`
- Database URL: `postgresql://weather-api:password@localhost/weather-api`
- CLI help: `Weather API - A comprehensive weather data API`

## Contributing to the Template

1. Fork the template repository
2. Make your improvements
3. Test with multiple project generations
4. Update documentation
5. Submit a pull request

## Support

- Check the generated project's README.md
- Report issues in the template repository
- Suggest improvements via GitHub issues
