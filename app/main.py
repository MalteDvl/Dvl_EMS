import requests
import time
import logging
from typing import Dict, Optional

# URL of Enpal.One
BASE_URL = "http://192.168.10.24"

# Endpoints for the required data
ENDPOINTS: Dict[str, str] = {
    "pv_production": "/api/pv/data/Power.DC.Total",
    "house_consumption": "/api/pv/data/Power.House.Total",
    "battery_power": "/api/pv/data/Power.Battery.Charge.Discharge",
    "grid_power": "/api/pv/data/Power.Grid.Export",
    "battery_level": "/api/pv/data/Energy.Battery.Charge.Level",
}

# Headers for the API request
HEADERS: Dict[str, str] = {"accept": "application/json", "Signature": "123"}


# Configure logging
class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.message = record.getMessage()
        return f"{self.formatTime(record, self.datefmt)}\n{record.message}"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = CustomFormatter(datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.handlers = [handler]


def get_ems_data(endpoint: str) -> Optional[float]:
    """Fetch data from the Ops Container API"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["number"]
    except requests.RequestException as e:
        logging.error(f"Error fetching data from {endpoint}: {e}")
        return None


def log_data(pv: float, battery: float, house: float, grid: float, battery_level: float) -> None:
    """Log the data in the specified format."""
    battery_status = "charging" if battery > 0 else "discharging"
    grid_status = "feeding in" if grid > 0 else "consuming"

    log_entry = (
        f"PV Production = {pv:.2f} W\n"
        f"Battery Power = {abs(battery):.2f} W ({battery_status})\n"
        f"House Consumption = {house:.2f} W\n"
        f"Grid Power = {abs(grid):.2f} W ({grid_status})\n"
        f"Battery Level = {battery_level:.2f}%\n"
        f"{'='*40}"
    )

    logging.info(log_entry)


def main() -> None:
    while True:
        data = {key: get_ems_data(endpoint) for key, endpoint in ENDPOINTS.items()}

        if all(data.values()):
            log_data(
                data["pv_production"],
                data["battery_power"],
                data["house_consumption"],
                data["grid_power"],
                data["battery_level"],
            )
        else:
            logging.warning("Failed to fetch all required data. Retrying in 30 seconds.")

        time.sleep(30)


if __name__ == "__main__":
    main()
