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
    def get_locations() -> List[Dict]:
        _data = make_request("locations", headers)
        return _data.get("results", [])
    return (get_locations,)


@app.cell
def _(get_locations):
    get_locations()
    return


@app.cell
def _(Dict, List, headers, make_request):
    def get_location_by_id(location_id) -> List[Dict]:
        location = "/locations" + "/" + f"{location_id}"
        _data = make_request(location, headers)
        print(_data)
        return _data.get("results", [])
    return (get_location_by_id,)


@app.cell
def _(get_location_by_id):
    get_location_by_id(18)
    return


@app.cell
def _(Dict, List, headers, make_request):
    def get_parameter_by_id(parameter_id) -> List[Dict]:
        parameter = "/parameters" + "/" + f"{parameter_id}"
        _data = make_request(parameter, headers)
        print(_data)
        return _data.get("results", [])
    return (get_parameter_by_id,)


@app.cell
def _(get_parameter_by_id):
    get_parameter_by_id(1)
    return


@app.cell
def _(Dict, List, headers, make_request):
    def get_parameters() -> List[Dict]:
        _data = make_request("parameters", headers)
        return _data.get("results", [])
    return (get_parameters,)


@app.cell
def _(get_parameters):
    get_parameters()
    return


@app.cell
def _(Dict, List, headers, make_request):
    def get_countries() -> List[Dict]:
        _data = make_request("countries", headers)
        return _data.get("results", [])
    return (get_countries,)


@app.cell
def _(get_countries):
    get_countries()
    return


@app.cell
def _(List, headers, make_request):
    def get_country_by_id(country_id) -> List:
        country = "/countries" + "/" + f"{country_id}"
        _data = make_request(country, headers)
        print(_data)
        return _data.get("results", [])
    return (get_country_by_id,)


@app.cell
def _(get_country_by_id):
    get_country_by_id(1)
    return


@app.cell
def _(Dict, List, headers, make_request):
    def parameters_latest_get(parameters_id) -> List[Dict]:
        parameter = (f"/parameters/{parameters_id}/latest")
        _data = make_request(parameter, headers)
        print(_data)
        return _data.get("results", [])
    return (parameters_latest_get,)


@app.cell
def _(parameters_latest_get):
    parameters_latest_get(1)
    return


@app.cell
def _(Dict, List, headers, make_request):
    # Provides a list of measurements by sensor ID
    def get_measurements_by_sensor_id(sensors_id) -> List[Dict]:
        sensors = (f"/sensors/{sensors_id}/measurements")
        _data = make_request(sensors, headers)
        print(_data)
        return _data.get("results", [])
    return (get_measurements_by_sensor_id,)


@app.cell
def _(get_measurements_by_sensor_id):
    get_measurements_by_sensor_id(9953017)
    return


@app.cell
def _(Dict, List, headers, make_request):
    # Get measurements aggregated to hours by sensor ID
    def get_measurements_by_sensor_id_hour(sensors_id) -> List[Dict]:
        sensors = (f"/sensors/{sensors_id}/measurements/hourly")
        _data = make_request(sensors, headers)
        print(_data)
        return _data.get("results", [])
    return (get_measurements_by_sensor_id_hour,)


@app.cell
def _(get_measurements_by_sensor_id_hour):
    get_measurements_by_sensor_id_hour(9953017)
    return


@app.cell
def _(Dict, List, headers, make_request):
    # Get measurements aggregated to days by sensor ID
    def get_measurements_by_sensor_id_daily(sensors_id) -> List[Dict]:
        sensors = (f"/sensors/{sensors_id}/measurements/daily")
        _data = make_request(sensors, headers)
        print(_data)
        return _data.get("results", [])
    return (get_measurements_by_sensor_id_daily,)


@app.cell
def _(get_measurements_by_sensor_id_daily):
    get_measurements_by_sensor_id_daily(9953017)
    return


@app.cell
def _(Dict, List, headers, make_request):
    # Get measurements aggregated to hour by sensor ID
    def get_measurements_by_sensor_id_hourly(sensors_id) -> List[Dict]:
        sensors = (f"/sensors/{sensors_id}/hours")
        _data = make_request(sensors, headers)
        print(_data)
        return _data.get("results", [])
    return (get_measurements_by_sensor_id_hourly,)


@app.cell
def _(get_measurements_by_sensor_id_hourly):
    get_measurements_by_sensor_id_hourly(9953017)
    return


@app.cell
def _(Dict, List, headers, make_request):
    # Get measurements aggregated from hour to day by sensor ID
    def get_measurements_by_sensor_id_hour_day(sensors_id) -> List[Dict]:
        sensors = (f"/sensors/{sensors_id}/hours/daily")
        _data = make_request(sensors, headers)
        print(_data)
        return _data.get("results", [])
    return (get_measurements_by_sensor_id_hour_day,)


@app.cell
def _(get_measurements_by_sensor_id_hour_day):
    get_measurements_by_sensor_id_hour_day(9953017)
    return


@app.cell
def _(Dict, List, headers, make_request):
    # Get measurements aggregated from hour to month by sensor ID
    def get_measurements_by_sensor_id_hour_month(sensors_id) -> List[Dict]:
        sensors = (f"/sensors/{sensors_id}/hours/monthly")
        _data = make_request(sensors, headers)
        print(_data)
        return _data.get("results", [])
    return (get_measurements_by_sensor_id_hour_month,)


@app.cell
def _(get_measurements_by_sensor_id_hour_month):
    get_measurements_by_sensor_id_hour_month(9953017)
    return


@app.cell
def _(Dict, List, headers, make_request):
    # Get measurements aggregated from hour to year by sensor ID
    def get_measurements_by_sensor_id_hour_year(sensors_id) -> List[Dict]:
        sensors = (f"/sensors/{sensors_id}/hours/yearly")
        _data = make_request(sensors, headers)
        print(_data)
        return _data.get("results", [])
    return (get_measurements_by_sensor_id_hour_year,)


@app.cell
def _(get_measurements_by_sensor_id_hour_year):
    get_measurements_by_sensor_id_hour_year(9953017)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
