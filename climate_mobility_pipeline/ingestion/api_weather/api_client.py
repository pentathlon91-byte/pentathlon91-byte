import requests
import logging

logger = logging.getLogger(__name__)

def fetch_weather_data(
    latitude,
    longitude,
    variables,
    start_date,
    end_date,
    timezone
):
    """
    Fetch hourly weather data from the Open-Meteo API for a specific date range.

    Parameters
    ----------
    latitude : float
        Geographic latitude of the location.
    longitude : float
        Geographic longitude of the location.
    variables : List[str]
        List of weather variables to request.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    timezone: str
        Timezone string.

    Returns
    -------
    dict
        Parsed JSON response containing hourly weather data.
    """
    
    base_url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(variables),
        "timezone": timezone,
        "start_date": start_date,
        "end_date": end_date
    }

    try:
        logger.info(f"Requesting weather data for {start_date} from Open-Meteo API...")

        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        logger.info("Weather data fetched successfully.")
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise
