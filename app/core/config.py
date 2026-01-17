"""
config.py
----------
Centralized application configuration using Pydantic's BaseSettings.

This module loads environment variables from the `.env` file (or the system
environment) and exposes them as strongly-typed attributes. The Settings class
provides a single source of truth for configurable values such as:

- SQL Server connection details
- User credentials (if SQL authentication is ever used)
- Future pipeline configuration options

Having all configuration in one place makes the project easier to maintain,
test, and deploy across development, staging, and production environments.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes
    ----------
    SQL_SERVER : str
        The SQL Server host or instance name. Supports formats such as:
        - 'DESKTOP-CQ2LR2P'
        - 'localhost'
        - '(local)'
        - '.'
        - 'servername\\instance'  (double-backslash required in .env)

    SQL_DATABASE : str
        The database name the ingestion pipelines will write into.

    SQL_USERNAME : Optional[str]
        Username for SQL authentication (not required when using
        Windows Trusted Authentication).

    SQL_PASSWORD : Optional[str]
        Password for SQL authentication (only used if SQL_USERNAME is set).

    Notes
    -----
    - Environment variables override default values.
    - Values are automatically loaded from `.env` per Config class below.
    """
    
    SQL_SERVER: str = "localhost\\SQLEXPRESS"  # default fallback
    SQL_DATABASE: str = "RawIngestion"         # default database
    SQL_USERNAME: str | None = None            # optional for SQL auth
    SQL_PASSWORD: str | None = None            # optional for SQL auth

    class Config:
        # This tells Pydantic to automatically load values from the .env file.
        env_file = ".env"


# Instantiate the global settings object.
# Import this anywhere in the codebase when configuration is needed.
settings = Settings()

