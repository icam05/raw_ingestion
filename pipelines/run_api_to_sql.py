"""
run_api_to_sql.py
------------------
Command-line entrypoint for the API → SQL Server ingestion pipeline.

This file allows the pipeline to be executed directly from the terminal using:

    python -m pipelines.run_api_to_sql

or by calling the script directly. Having a dedicated runner script makes
testing, scheduling (e.g., Windows Task Scheduler, cron, Airflow), and
automation straightforward, without requiring the FastAPI server to run.
"""

from app.ingestion.pipelines.api_to_sql import run_pipeline


if __name__ == "__main__":
    # Run the ingestion pipeline end-to-end.
    # This structure follows the common Python "entrypoint" pattern and
    # enables proper execution when the module is invoked with -m.
    run_pipeline()
