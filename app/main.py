import time
import logging
import argparse
from app.enpalone_api import get_all_enpalone_data
from app.config import DATA_FETCH_INTERVAL


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            self._style._fmt = "%(asctime)s\n%(message)s"
        else:
            self._style._fmt = "%(asctime)s - %(levelname)s - %(message)s"
        return super().format(record)


def setup_logging(debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(level)

    handler = logging.StreamHandler()
    formatter = CustomFormatter(datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def log_data(pv: float, battery: float, house: float, grid: float, battery_level: float) -> None:
    """Log the Enpal.One data in the specified format."""
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


def main(debug: bool = False) -> None:

    setup_logging(debug)

    while True:
        try:
            data = get_all_enpalone_data()
            logging.debug(f"Received data: {data}")

            if all(v is not None for v in data.values()):
                log_data(
                    data["pv_production"],
                    data["battery_power"],
                    data["house_consumption"],
                    data["grid_power"],
                    data["battery_level"],
                )
            else:
                logging.warning(f"Failed to fetch all required data. Received data: {data}")

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

        time.sleep(DATA_FETCH_INTERVAL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enpal.One data logger")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    main(debug=args.debug)
