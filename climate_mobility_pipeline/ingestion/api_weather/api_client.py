import requests
import logging

# Module-level logger for consistent, structured logging
logger = logging.getLogger(__name__)

def fetch_weather_data(latitude, longitude, variables):
    """
    Fetch hourly weather data from the Open-Meteo API.

    Parameters
    ----------
    latitude : float
        Geographic latitude of the location.
    longitude : float
        Geographic longitude of the location.
    variables : List[str]
        List of weather variables to request (e.g. ["temperature_2m", "windspeed_10m"]).

    Returns
    -------
    dict
        Parsed JSON response containing hourly weather data.

    Notes
    -----
    This function is responsible ONLY for making the API request.
    It does not handle local storage, Azure upload, or configuration.
    """
    
    # Base endpoint for the Open-Meteo forecast API
    base_url = "https://api.open-meteo.com/v1/forecast"

    # Query parameters for the API request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(variables),   # API expects comma-separated string
        "timezone": "auto"               # Automatically adjusts timestamps to local timezone
    }

    try:
        logger.info("Requesting weather data from Open-Meteo API...")

        # Perform the HTTP GET request with a timeout for safety
        response = requests.get(base_url, params=params, timeout=10)

        # Raise an exception for HTTP errors (4xx, 5xx)
        response.raise_for_status()

        logger.info("Weather data fetched successfully.")
        return response.json()

    except requests.exceptions.RequestException as e:
        # Catch all network-related errors (timeouts, connection issues, invalid responses)
        logger.error(f"API request failed: {e}")
        raise
