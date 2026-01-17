"""
main.py
--------
Application entrypoint for the Raw Ingestion Service.

This module initializes the FastAPI application, configures metadata,
and registers all API routers. It acts as the top-level API layer
exposing endpoints for orchestration (e.g., triggering ingestion jobs).

Structure:
- Create the FastAPI app instance
- Attach API routers (modular structure for expandability)
- Define a root health-check endpoint

This keeps the project clean, modular, and easy to scale as new pipelines
or features are added.
"""

from fastapi import FastAPI
from app.api.ingestion_router import router as ingestion_router


# ------------------------------------------------------------------------------
# FastAPI Application Initialization
# ------------------------------------------------------------------------------
# The main FastAPI app for the ingestion platform.
# Metadata (title, version) is visible in Swagger docs and helps consumers
# understand what the service is responsible for.
app = FastAPI(
    title="Raw Ingestion Service",
    version="1.0.0",
    description="A modular ingestion engine capable of pulling data from APIs, "
                "files, and databases into SQL Server."
)


# ------------------------------------------------------------------------------
# Register Routers
# ------------------------------------------------------------------------------
# Routers allow you to organize API endpoints by feature area.
# The ingestion router houses endpoints that trigger pipelines
# (API → SQL, CSV → SQL, DB → DB, etc.)
app.include_router(
    ingestion_router,
    prefix="/ingest",
    tags=["ingestion"]
)


# ------------------------------------------------------------------------------
# Root Endpoint (Health Check)
# ------------------------------------------------------------------------------
# Lightweight endpoint used for:
# - determining whether the service is online
# - verifying that FastAPI started successfully
# - uptime/load-balancer checks
#
# Returns a simple JSON payload.
@app.get("/")
def root():
    return {"status": "ok", "service": "raw_ingestion"}

