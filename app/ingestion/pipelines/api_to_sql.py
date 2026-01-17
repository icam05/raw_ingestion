"""
api_to_sql.py
--------------
Pipeline module: API → SQL Server

This pipeline demonstrates a complete ingestion workflow:
1. Extract data from an external REST API
2. Transform the payload into a clean Pandas DataFrame
3. Load the final dataset into a SQL Server staging table

Pipelines are intentionally kept lightweight and orchestrate only:
- the order of operations
- error/validation handling (expandable)
- logging and observability
- calls to connectors and loaders

This matches real-world data engineering patterns where pipelines
coordinate work done by specialized components.
"""

from app.ingestion.connectors.api_connector import fetch_posts
from app.ingestion.loaders.sql_loader import load_dataframe


def run_pipeline() -> None:
    """
    Execute the API → SQL ingestion pipeline.

    Steps
    -----
    1. Call the REST API connector to retrieve raw post data.
    2. Convert the response into a DataFrame.
    3. Write the data into SQL Server (staging layer).
    4. Log progress and completion.

    Notes
    -----
    - This function is intentionally synchronous and simple.
      In production, this could be expanded with:
        • try/except blocks for error handling
        • logging frameworks (e.g., structlog, loguru)
        • orchestration (Airflow, Prefect, Dagster)
        • incremental extraction logic
        • data quality checks before loading
    """

    # ----------------------------------------------------------------------
    # 1. Extract: Fetch data from external REST API
    # ----------------------------------------------------------------------
    df = fetch_posts()
    print(f"[api_to_sql] API rows fetched: {len(df)}")

    # ----------------------------------------------------------------------
    # 2. Load: Persist into SQL Server staging table
    # ----------------------------------------------------------------------
    load_dataframe("stg_ApiPosts", df, mode="replace")

    # ----------------------------------------------------------------------
    # Final status
    # ----------------------------------------------------------------------
    print("[api_to_sql] Pipeline complete.")
