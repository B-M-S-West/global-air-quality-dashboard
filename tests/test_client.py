import pytest
from unittest.mock import patch, MagicMock
from unittest.mock import patch, call
from src.api.client import OpenAQClient
from datetime import datetime


@pytest.fixture
def client():
    return OpenAQClient()


@patch("src.api.client.OpenAQClient._make_request")
def test_get_countries(mock_make_request, client):
    mock_make_request.return_value = {
        "results": [{"code": "US", "name": "United States"}]
    }
    result = client.get_countries()
    mock_make_request.assert_called_with("countries")
    assert result == [{"code": "US", "name": "United States"}]


@patch("src.api.client.OpenAQClient._make_request")
def test_get_locations(mock_make_request, client):
    mock_make_request.return_value = {"results": [{"id": 1, "name": "Loc1"}]}
    bbox = (1.0, 2.0, 3.0, 4.0)
    result = client.get_locations(country="US", bbox=bbox)
    expected_params = {
        "limit": 1000,
        "country": "US",
        "bbox": "1.0,2.0,3.0,4.0",
    }
    mock_make_request.assert_called_with("locations", expected_params)
    assert result == [{"id": 1, "name": "Loc1"}]


@patch("src.api.client.OpenAQClient._make_request")
def test_get_parameters(mock_make_request, client):
    mock_make_request.return_value = {"results": [{"id": 1, "name": "pm25"}]}
    result = client.get_parameters()
    mock_make_request.assert_called_with("parameters")
    assert result == [{"id": 1, "name": "pm25"}]


@patch("src.api.client.OpenAQClient._make_request")
def test_get_latest_measurements(mock_make_request, client):
    mock_make_request.return_value = {"results": [{"location": "A"}]}
    result = client.get_latest_measurements(
        location_ids=[1, 2], countries=["US"], parameters=["pm25"]
    )
    expected_calls = [
        call("locations/1/latest", {"limit": 1000, "countries": "US", "parameters": "pm25"}),
        call("locations/2/latest", {"limit": 1000, "countries": "US", "parameters": "pm25"})
    ]
    
    mock_make_request.assert_has_calls(expected_calls, any_order=True)

    assert result == [{"location": "A"}, {"location": "A"}]


@patch("src.api.client.OpenAQClient._make_request")
def test_get_measurements(mock_make_request, client):
    mock_make_request.return_value = {"results": [{"value": 10}]}
    date_from = datetime(2024, 1, 1)
    date_to = datetime(2024, 1, 2)
    result = client.get_measurements(
        location_id=1, parameter="pm25", date_from=date_from, date_to=date_to, limit=500
    )
    expected_params = {
        "limit": 500,
        "sort": "datetime",
        "locations": 1,
        "parameters": "pm25",
        "date_from": date_from.isoformat(),
        "date_to": date_to.isoformat(),
    }
    mock_make_request.assert_called_with("measurements", expected_params)
    assert result == [{"value": 10}]


@patch("src.api.client.OpenAQClient._make_request")
def test_get_location_measurements_aggregated(mock_make_request, client):
    mock_make_request.return_value = {"results": [{"avg": 5}]}
    date_from = datetime(2024, 1, 1)
    date_to = datetime(2024, 1, 2)
    result = client.get_location_measurements_aggregated(
        location_id=1,
        parameter="pm25",
        period="hour",
        date_from=date_from,
        date_to=date_to,
    )
    expected_endpoint = "locations/1/measurements/hours"
    expected_params = {
        "parameters": "pm25",
        "date_from": date_from.isoformat(),
        "date_to": date_to.isoformat(),
    }
    mock_make_request.assert_called_with(expected_endpoint, expected_params)
    assert result == [{"avg": 5}]
