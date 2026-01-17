"""
api_connector.py
-----------------
REST API connector module.

This file contains functions responsible for retrieving data from external
HTTP APIs. Each connector is intentionally lightweight, handling only:

1. Network requests
2. Validation of the HTTP response
3. Conversion of raw JSON into Pandas DataFrames

Business logic, transformations, and loading are handled elsewhere in the
pipeline layers. This separation of concerns follows data engineering
best practices and keeps the ingestion architecture modular and scalable.
"""

import requests
import pandas as pd


def fetch_posts() -> pd.DataFrame:
    """
    Fetch example post data from the JSONPlaceholder REST API.

    This function demonstrates a simple REST API ingestion pattern:
    - Issue an HTTP GET request to a public API endpoint
    - Validate the response status
    - Convert returned JSON into a normalized Pandas DataFrame

    Returns
    -------
    pd.DataFrame
        A DataFrame containing one row per post, with flattened JSON fields.

    Raises
    ------
    HTTPError
        If the network request returns a non-200 response.
    RequestException
        For network-level issues such as DNS failures or timeouts.

    Notes
    -----
    • JSONPlaceholder is used here as a test/dummy API.
    • In real-world ingestion systems, this connector would include:
        - authentication (OAuth2, bearer tokens, API keys)
        - pagination handling
        - incremental extraction (timestamps or IDs)
        - rate limiting / retry logic
    """
    url = "https://jsonplaceholder.typicode.com/posts"

    # Send GET request with timeout to avoid hanging ingestion jobs
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # Automatically raises an exception for error codes

    # Convert JSON list-of-dicts into a normalized DataFrame
    data = response.json()
    return pd.json_normalize(data)
