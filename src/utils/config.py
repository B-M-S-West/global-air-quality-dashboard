"""Configuration management for OpenAQ Dashboard."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for OpenAQ Dashboard."""

    # API Configuration
    OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY", "")
    OPENAQ_BASE_URL = os.getenv("OPENAQ_BASE_URL", "https://api.openaq.org/v3")

    # Rate limiting
    REQUESTS_PER_MINUTE = 60
    REQUESTS_PER_HOUR = 2000

    # Dashboard settings
    DEFAULT_POLLUTANTS = ["pm25", "pm10", "no2", "o3", "co", "so2"]

    # Map settings
    DEFAULT_MAP_CENTER = [40.7128, -74.0060]  # New York City
    DEFAULT_MAP_ZOOM = 2

    # Data refresh intervals (in seconds)
    CACHE_TIMEOUT = 300  # 5 minutes

    @classmethod
    def validate_api_key(cls):
        """Validate that API key is configured."""
        if not cls.OPENAQ_API_KEY:
            raise ValueError(
                "OpenAQ API key not configured. Please set OPENAQ_API_KEY environment variable."
            )
        return True


# Pollutant metadata
POLLUTANT_INFO = {
    "pm25": {
        "display_name": "PM2.5",
        "description": "Fine particulate matter (≤ 2.5 micrometers)",
        "units": "µg/m³",
        "color": "#FF6B6B",
    },
    "pm10": {
        "display_name": "PM10",
        "description": "Inhalable particulate matter (≤ 10 micrometers)",
        "units": "µg/m³",
        "color": "#4ECDC4",
    },
    "no2": {
        "display_name": "NO₂",
        "description": "Nitrogen dioxide",
        "units": "ppm",
        "color": "#45B7D1",
    },
    "o3": {
        "display_name": "O₃",
        "description": "Ground-level ozone",
        "units": "ppm",
        "color": "#96CEB4",
    },
    "co": {
        "display_name": "CO",
        "description": "Carbon monoxide",
        "units": "ppm",
        "color": "#FFEAA7",
    },
    "so2": {
        "display_name": "SO₂",
        "description": "Sulfur dioxide",
        "units": "ppm",
        "color": "#DDA0DD",
    },
    "bc": {
        "display_name": "BC",
        "description": "Black Carbon",
        "units": "µg/m³",
        "color": "#2C3E50",
    },
}

# Air Quality Index thresholds (for PM2.5 as example)
AQI_THRESHOLDS = {
    "pm25": [
        (0, 12, "Good", "#00E400"),
        (12.1, 35.4, "Moderate", "#FFFF00"),
        (35.5, 55.4, "Unhealthy for Sensitive Groups", "#FF7E00"),
        (55.5, 150.4, "Unhealthy", "#FF0000"),
        (150.5, 250.4, "Very Unhealthy", "#8F3F97"),
        (250.5, float("inf"), "Hazardous", "#7E0023"),
    ]
}
