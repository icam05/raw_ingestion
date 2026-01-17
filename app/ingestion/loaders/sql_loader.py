"""
sql_loader.py
--------------
SQL Server loader utilities.

This module is responsible for taking in-memory Pandas DataFrames and
persisting them into SQL Server tables. It encapsulates:

- Construction of a SQLAlchemy engine using an ODBC connection string
- Bulk insert operations via `DataFrame.to_sql`
- Simple safeguards (e.g., skip empty DataFrames)

By centralizing SQL write operations here, pipelines remain focused on
business logic (what to load and when), while this loader handles the
mechanics of *how* data is persisted.
"""

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

from app.core.config import settings


def get_engine():
    """
    Create and return a SQLAlchemy engine for SQL Server.

    The connection string is built using an ODBC connection string
    and then URL-encoded for SQLAlchemy. This approach:

    - Supports local/default instances (e.g., localhost, .)
    - Works smoothly with Windows Trusted Authentication
    - Avoids issues with backslashes in instance names

    Returns
    -------
    sqlalchemy.engine.Engine
        A SQLAlchemy engine configured for SQL Server with fast_executemany enabled.
    """
    # Base ODBC connection string. Values are supplied from central Settings.
    odbc_str = (
        f"DRIVER=ODBC Driver 17 for SQL Server;"
        f"SERVER={settings.SQL_SERVER};"
        f"DATABASE={settings.SQL_DATABASE};"
        "Trusted_Connection=yes;"
    )

    # URL-encode the ODBC string for use with SQLAlchemy's pyodbc dialect.
    connect_str = "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_str)

    # fast_executemany=True significantly improves performance on bulk inserts.
    return create_engine(connect_str, fast_executemany=True)


def load_dataframe(table: str, df: pd.DataFrame, mode: str = "replace") -> None:
    """
    Load a Pandas DataFrame into a SQL Server table.

    Parameters
    ----------
    table : str
        Target table name in SQL Server (e.g., 'stg_ApiPosts').
    df : pd.DataFrame
        DataFrame to be written into SQL Server.
    mode : str, optional
        Behavior when the target table already exists:
        - 'replace' : drop the table and recreate it (default)
        - 'append'  : append rows to the existing table

    Notes
    -----
    - If the DataFrame is empty, the function logs a message and returns.
    - Schema inference is handled by Pandas/SQLAlchemy.
    - In a production environment, this can be extended to:
        • enforce explicit schemas
        • wrap operations in transactions
        • add logging/metrics (e.g., row counts, duration)
    """
    if df.empty:
        print(f"[sql_loader] No data to load into '{table}'. Skipping write.")
        return

    engine = get_engine()

    # Use Pandas' built-in SQL integration to persist the DataFrame.
    df.to_sql(table, engine, if_exists=mode, index=False)

    print(f"[sql_loader] Loaded {len(df)} rows into '{table}' (mode='{mode}').")
