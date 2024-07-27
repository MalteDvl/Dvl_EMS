import time
import logging
from datetime import datetime
from multiprocessing import Process, Queue
from app.enpalone_api import get_all_enpalone_data
from app.config import DATA_FETCH_INTERVAL
from app.flask_app import run_flask_app

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Set Flask's logger to WARNING level
logging.getLogger("werkzeug").setLevel(logging.WARNING)


def log_data_to_console(pv: float, battery: float, house: float, grid: float, battery_level: float) -> None:
    """Log the Enpal.One data in the specified format."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if battery > 0:
        battery_status = "(charging)"
    elif battery < 0:
        battery_status = "(discharging)"
    else:
        battery_status = ""

    if grid > 0:
        grid_status = "(feeding in)"
    elif grid < 0:
        grid_status = "(consuming)"
    else:
        grid_status = ""

    log_entry = (
        f"{now}\n"
        f"PV Production = {int(pv)} W\n"
        f"Battery Power = {int(abs(battery))} W {battery_status}\n"
        f"House Consumption = {int(house)} W\n"
        f"Grid Power = {int(abs(grid))} W {grid_status}\n"
        f"Battery Level = {battery_level:.1f} %\n"
        f"{'='*40}"
    )

    logger.info(log_entry)


def data_logging_process(queue):
    while True:
        try:
            data = get_all_enpalone_data()
            if all(v is not None for v in data.values()):
                log_data_to_console(
                    data["pv_production"],
                    data["battery_power"],
                    data["house_consumption"],
                    data["grid_power"],
                    data["battery_level"],
                )
                queue.put(data)
            else:
                logger.warning(f"Failed to fetch all required data. Received data: {data}")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")

        time.sleep(DATA_FETCH_INTERVAL)


if __name__ == "__main__":
    data_queue = Queue()

    # Start the data logging process
    logging_process = Process(target=data_logging_process, args=(data_queue,))
    logging_process.start()

    # Start the Flask app process
    flask_process = Process(target=run_flask_app, args=(data_queue,))
    flask_process.start()

    # Wait for both processes
    logging_process.join()
    flask_process.join()
