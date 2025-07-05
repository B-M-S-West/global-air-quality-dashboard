import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import httpx
    import time
    from datetime import datetime
    from typing import Dict, List, Tuple
    from dotenv import load_dotenv
    import os
    return Dict, List, httpx, load_dotenv, os


@app.cell
def _(load_dotenv, os):
    load_dotenv()
    # API Configuration
    api_key = os.getenv("OPENAQ_API_KEY", "")
    base_url = os.getenv("OPENAQ_BASE_URL", "https://api.openaq.org/v3")
    headers = {"X-API-KEY": api_key}
    return base_url, headers


@app.cell
def _():
    # Rate limiting
    REQUESTS_PER_MINUTE = 60
    REQUESTS_PER_HOUR = 2000

    # Dashboard settings
    DEFAULT_POLLUTANTS = ["pm25", "pm10", "no2", "o3", "co", "so2"]

    # Map settings
    DEFAULT_MAP_CENTER = [40.7128, -74.0060]  # New York City
    DEFAULT_MAP_ZOOM = 2

    # Data refresh intervals (in seconds)
    CACHE_TIMEOUT = 300 
    return


@app.cell
def _(Dict, base_url, httpx):
    def make_request(endpoint: str, headers: Dict, params: Dict = None) -> Dict:
        url = f"{base_url}/{endpoint.lstrip('/')}"
        response = httpx.get(url, headers=headers, params=params or {})
        return response.json()
    return (make_request,)


@app.cell
def _(Dict, List, headers, make_request):
    def get_countries() -> List[Dict]:
        data = make_request("countries", headers)
        return data.get("results", [])
    return (get_countries,)


@app.cell
def _(get_countries):
    get_countries()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
