import requests
from typing import Dict, Optional
import logging
from app.config import ENPALONE_URL, ENPALONE_ENDPOINTS, ENPALONE_HEADERS

logger = logging.getLogger(__name__)


def get_enpalone_data(endpoint: str) -> Optional[float]:
    """Fetch data from the Enpal.One API"""
    try:
        url = f"{ENPALONE_URL}{endpoint}"
        logger.debug(f"Attempting to fetch data from: {url}")
        response = requests.get(url, headers=ENPALONE_HEADERS, timeout=10)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")
        response.raise_for_status()
        data = response.json()
        return data["number"]
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error when fetching data from {endpoint}: {e}")
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error when fetching data from {endpoint}: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from {endpoint}: {e}")
    except KeyError as e:
        logger.error(f"Unexpected response format from {endpoint}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error when fetching data from {endpoint}: {e}")
    return None


def get_all_enpalone_data() -> Dict[str, Optional[float]]:
    """Fetch all Enpal.One data"""
    return {key: get_enpalone_data(endpoint) for key, endpoint in ENPALONE_ENDPOINTS.items()}
