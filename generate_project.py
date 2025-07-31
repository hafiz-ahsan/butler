#!/usr/bin/env python3
"""
Project template generator script.
Generates a new project from the template by replacing template variables.
"""

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Any


def load_template_config() -> Dict[str, Any]:
    """Load the template configuration."""
    config_path = Path(__file__).parent / "template_config.json"
    with open(config_path) as f:
        return json.load(f)


def get_user_config() -> Dict[str, Any]:
    """Get configuration from user input."""
    print("Python Backend Service Template Generator")
    print("=" * 50)
    
    config = {}
    
    # Required fields
    config["project_name"] = input("Project name (lowercase, no spaces): ").lower().replace(" ", "-")
    config["project_name_title"] = input(f"Project title [{config['project_name'].title()}]: ") or config['project_name'].title()
    config["project_description"] = input("Project description: ") or f"A Python backend service"
    config["author_name"] = input("Author name: ") or "Your Team"
    config["author_email"] = input("Author email: ") or "team@example.com"
    
    # Optional fields with defaults
    config["github_repo"] = input(f"GitHub repo [{config['author_name'].lower().replace(' ', '-')}/{config['project_name']}]: ") or f"{config['author_name'].lower().replace(' ', '-')}/{config['project_name']}"
    config["database_name"] = config["project_name"]
    config["database_user"] = config["project_name"]
    config["service_description"] = f"{config['project_name_title']} - {config['project_description']}"
    config["cli_description"] = f"{config['project_name_title']} - {config['project_description']}"
    
    # Fix author name for email template replacement
    if "Team" not in config["author_name"]:
        config["author_name"] = f"{config['author_name']} Team"
    
    return config


def replace_in_file(file_path: Path, replacements: Dict[str, str]) -> None:
    """Replace template variables in a file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        file_path.write_text(content, encoding='utf-8')
        print(f"Updated {file_path}")
        
    except UnicodeDecodeError:
        # Skip binary files
        print(f"Skipped binary file {file_path}")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")


def rename_directories(base_path: Path, old_name: str, new_name: str) -> None:
    """Rename directories containing the old project name."""
    for root, dirs, files in os.walk(base_path, topdown=False):
        root_path = Path(root)
        
        # Rename directories
        for dir_name in dirs:
            if old_name in dir_name:
                old_dir = root_path / dir_name
                new_dir = root_path / dir_name.replace(old_name, new_name)
                if old_dir.exists() and not new_dir.exists():
                    old_dir.rename(new_dir)
                    print(f"Renamed directory: {old_dir} -> {new_dir}")


def generate_project(target_dir: str = None) -> None:
    """Generate a new project from the template."""
    template_config = load_template_config()
    user_config = get_user_config()
    
    # Determine target directory
    if target_dir is None:
        target_dir = input(f"\nTarget directory [{user_config['project_name']}]: ") or user_config['project_name']
    
    target_path = Path(target_dir).resolve()
    
    if target_path.exists():
        response = input(f"Directory {target_path} exists. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    else:
        target_path.mkdir(parents=True, exist_ok=True)
    
    # Copy template to target directory (if not generating in place)
    source_path = Path(__file__).parent
    if target_path != source_path:
        print(f"Copying template to {target_path}...")
        
        # Copy files, excluding certain directories and files
        exclude_patterns = {
            '.git', '__pycache__', '.pytest_cache', '.venv', '.mypy_cache',
            'htmlcov', '.coverage', 'generate_project.py', 'template_config.json',
            'test-api'  # Don't copy previously generated test directories
        }
        
        for item in source_path.iterdir():
            if item.name not in exclude_patterns:
                if item.is_dir():
                    shutil.copytree(item, target_path / item.name, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, target_path / item.name)
    
    # Create replacement mappings
    replacements = {}
    for key, value in template_config.items():
        if key in user_config:
            replacements[value] = user_config[key]
    
    print(f"\nApplying template transformations...")
    print(f"Replacements: {replacements}")
    
    # Apply replacements to all text files
    for root, dirs, files in os.walk(target_path):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.pytest_cache', '.venv', '.mypy_cache', 'htmlcov'}]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in {'.py', '.toml', '.yaml', '.yml', '.json', '.md', '.txt', '.sh', '.conf', '.cfg', '.ini', '.Dockerfile'}:
                replace_in_file(file_path, replacements)
    
    # Rename directories
    old_project_name = template_config['project_name']
    new_project_name = user_config['project_name']
    
    if old_project_name != new_project_name:
        rename_directories(target_path, old_project_name, new_project_name)
    
    # Clean up template files
    template_files = [
        target_path / 'generate_project.py',
        target_path / 'template_config.json'
    ]
    
    for file in template_files:
        if file.exists():
            file.unlink()
            print(f"Removed template file: {file}")
    
    print(f"\nProject '{user_config['project_name_title']}' generated successfully!")
    print(f"Location: {target_path}")
    print(f"\nNext steps:")
    print(f"   cd {target_path}")
    print(f"   make install-dev")
    print(f"   make dev")


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    generate_project(target_dir)