Raw Ingestion Service

A modular, extensible data ingestion engine built with FastAPI, Python, Pandas, and SQL Server, designed to demonstrate professional data-engineering patterns including connectors, pipelines, loaders, orchestration, and automation.

This project ingests data from multiple sources (REST APIs, SQL Server, CSV files, future data sources) and loads them into a SQL Server staging layer, following production-grade architecture and separation of concerns.

Project Purpose

This repository serves as a portfolio-quality demonstration of:

Real-world data engineering design

Modular ingestion pipelines

REST API extraction

SQL Server loading and staging

Separation of connectors, pipelines, loaders, and orchestration

FastAPI-based pipeline triggering

CLI-based batch execution

Environment-driven configuration

It is intentionally structured like a production ingestion microservice used in modern data engineering teams.

raw_ingestion/
│
├── app/
│ ├── api/ # FastAPI routers (pipeline orchestration)
│ ├── core/ # Configuration management
│ ├── db/ # Reserved for SQLAlchemy models (future use)
│ ├── ingestion/
│ │ ├── connectors/ # Source systems (API, DB, files, GitHub)
│ │ ├── loaders/ # Load targets (SQL Server, files)
│ │ ├── pipelines/ # End-to-end ingestion workflows
│ │ └── schemas/ # Pydantic schemas (future validation)
│ └── main.py # FastAPI application entrypoint
│
├── pipelines/ # CLI entrypoints for batch execution
│
├── sql/ # SQL scripts (staging table creation, merges)
│
├── config/ # YAML config (future job scheduling)
│
├── .env # Environment variables (local settings)
├── .env.example # Template for environment variables
└── README.md # Documentation (this file)

Architectural Overview

The ingestion system is built around five core concepts:

1. Connectors (Source-specific extraction)

Each connector retrieves data from a specific system:

REST API (api_connector)

SQL Server (future)

CSV/Parquet (filesystem_connector, future)

GitHub (github_csv, future)

2. Loaders (Target-specific persistence)

Loaders have a single responsibility: write DataFrames to a target system such as:

SQL Server

Filesystem (CSV/Parquet)

S3/Azure Blob (future)

3. Pipelines (Business workflows)

Pipelines orchestrate the following:

Extract → Transform → Load

Error handling (future)

Incremental logic (future)

Multi-source unification (future)

4. FastAPI as the orchestration layer

FastAPI provides a clean interface to:

Trigger pipelines

Expose routes for batch processes

Integrate with schedulers or external services

5. CLI batch runner (automation-ready)

Pipelines can be executed from:

Windows Task Scheduler

Airflow

Cron

Azure Automation

AWS Lambda or containers
