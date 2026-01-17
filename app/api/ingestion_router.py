"""
ingestion_router.py
--------------------
Exposes API endpoints that trigger ingestion pipelines.

This router acts as the orchestration layer for the ingestion engine.
Each endpoint corresponds to a specific pipeline (API → SQL, CSV → SQL,
DB → Files, etc.). By separating pipeline execution from the routing logic,
we maintain a clean, scalable architecture.

FastAPI automatically includes these routes under the prefix defined in
`main.py`, making it easy to manage and discover ingestion tasks.
"""

from fastapi import APIRouter
from app.ingestion.pipelines.api_to_sql import run_pipeline


# ------------------------------------------------------------------------------
# Router Initialization
# ------------------------------------------------------------------------------
# A dedicated router helps keep the API modular and organized. New pipelines
# can be added simply by creating new endpoints here.
router = APIRouter()


# ------------------------------------------------------------------------------
# Ingestion Pipeline Endpoints
# ------------------------------------------------------------------------------

@router.post("/api-to-sql/run")
def trigger_api_to_sql() -> dict:
    """
    Trigger the API → SQL ingestion pipeline.

    This endpoint executes the `run_pipeline()` function, which performs:
    - API extraction
    - DataFrame transformation
    - SQL Server loading into a staging table

    Returns
    -------
    dict
        Confirmation that the pipeline completed successfully.
    """
    run_pipeline()
    return {"status": "complete", "pipeline": "api_to_sql"}
