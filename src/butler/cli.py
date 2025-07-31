"""CLI interface for Butler service."""

import asyncio
from typing import Optional

import typer
import uvicorn
from rich.console import Console
from rich.table import Table

from butler.core.config import settings
from butler.core.logging import configure_logging, get_logger

app = typer.Typer(name="butler", help="Butler - A Python backend service")
console = Console()


@app.command()
def serve(
    host: str = typer.Option(settings.host, help="Host to bind to"),
    port: int = typer.Option(settings.port, help="Port to bind to"),
    reload: bool = typer.Option(settings.reload, help="Enable auto-reload"),
    workers: int = typer.Option(settings.workers, help="Number of worker processes"),
    log_level: str = typer.Option(settings.log_level, help="Log level"),
):
    """Start the Butler service."""
    console.print(f"Starting Butler service on {host}:{port}", style="bold green")
    
    uvicorn.run(
        "butler.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
        log_level=log_level.lower(),
    )


@app.command()
def config():
    """Show current configuration."""
    configure_logging()
    
    # Create a table to display configuration
    table = Table(title="Butler Configuration")
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    # Add configuration rows
    config_items = [
        ("App Name", settings.app_name),
        ("Version", settings.app_version),
        ("Debug", str(settings.debug)),
        ("Host", settings.host),
        ("Port", str(settings.port)),
        ("Workers", str(settings.workers)),
        ("Database URL", settings.database_url),
        ("Redis URL", settings.redis_url),
        ("Log Level", settings.log_level),
        ("OpenAI API Key", "Set" if settings.openai_api_key else "Not Set"),
        ("Anthropic API Key", "Set" if settings.anthropic_api_key else "Not Set"),
        ("Google AI API Key", "Set" if settings.google_ai_api_key else "Not Set"),
    ]
    
    for setting, value in config_items:
        table.add_row(setting, value)
    
    console.print(table)


@app.command()
def health():
    """Check service health."""
    import httpx
    
    try:
        response = httpx.get(f"http://{settings.host}:{settings.port}/health")
        if response.status_code == 200:
            data = response.json()
            console.print("Service is healthy", style="bold green")
            console.print(f"Status: {data['status']}")
            console.print(f"Version: {data['version']}")
        else:
            console.print(f"Service unhealthy: {response.status_code}", style="bold red")
    except Exception as e:
        console.print(f"Unable to connect to service: {e}", style="bold red")


@app.command()
def test():
    """Run tests."""
    import subprocess
    import sys
    
    console.print("Running tests...", style="bold blue")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--cov=butler",
            "--cov-report=term-missing"
        ], check=True)
        console.print("All tests passed!", style="bold green")
    except subprocess.CalledProcessError:
        console.print("Tests failed!", style="bold red")
        raise typer.Exit(1)


@app.command()
def lint():
    """Run linting checks."""
    import subprocess
    import sys
    
    console.print("Running linting checks...", style="bold blue")
    
    commands = [
        (["black", "--check", "--diff", "."], "Black formatting"),
        (["isort", "--check-only", "--diff", "."], "Import sorting"),
        (["flake8", "."], "Flake8 linting"),
        (["mypy", "src/butler"], "Type checking"),
    ]
    
    failed = False
    for cmd, description in commands:
        console.print(f"Running {description}...")
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            console.print(f"{description} passed", style="green")
        except subprocess.CalledProcessError as e:
            console.print(f"{description} failed", style="red")
            if e.stdout:
                console.print(e.stdout.decode())
            if e.stderr:
                console.print(e.stderr.decode())
            failed = True
    
    if failed:
        raise typer.Exit(1)
    else:
        console.print("All linting checks passed!", style="bold green")


if __name__ == "__main__":
    app()