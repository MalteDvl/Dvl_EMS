import sys
import time
import logging
from datetime import datetime
from multiprocessing import Process, Queue
from app.enpalone_api import get_all_enpalone_data
from app.fritz_api import get_socket_state, switch_fritz_device
from app.config import DATA_FETCH_INTERVAL

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Correctly handle password without importing from config.py
if len(sys.argv) != 2:
    print("Usage: python main.py <PASSWORD>")
    sys.exit(1)

password = sys.argv[1]  # Use the password provided by command line


def log_data_to_console(data, socket_status):
    """Logs the data and socket status."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    battery_status = "(charging)" if data["battery_power"] > 0 else "(discharging)" if data["battery_power"] < 0 else ""
    grid_status = "(feeding in)" if data["grid_power"] > 0 else "(consuming)" if data["grid_power"] < 0 else ""

    log_entry = (
        f"{now}\n"
        f"PV Production = {int(data['pv_production'])} W\n"
        f"Battery Power = {int(data['battery_power'])} W {battery_status}\n"
        f"House Consumption = {int(data['house_consumption'])} W\n"
        f"Grid Power = {int(data['grid_power'])} W {grid_status}\n"
        f"Battery Level = {data['battery_level']:.1f} %\n"
        f"Socket Status = {'On' if socket_status == '1' else 'Off'}\n"
        f"{'='*40}"
    )
    logger.info(log_entry)


def check_and_switch_socket(data, password):
    """Checks the house power and switches the socket if necessary."""
    house_power = data.get("house_consumption", 0)
    current_status = get_socket_state(password)[1]  # '1' or '0'
    logger.debug(f"House power: {house_power} W, Current Socket Status: {current_status}")

    if house_power < 1000 and current_status == "0":
        logger.debug("House power below 1000 W and socket is off, turning on.")
        status_code, response = switch_fritz_device("setswitchon", password)
        if status_code == 200:
            logger.debug("Socket turned on successfully.")
            return "1"  # Switch is now on
    elif house_power > 1000 and current_status == "1":
        logger.debug("House power above 1000 W and socket is on, turning off.")
        status_code, response = switch_fritz_device("setswitchoff", password)
        if status_code == 200:
            logger.debug("Socket turned off successfully.")
            return "0"  # Switch is now off

    return current_status  # Return current status if no action is taken


def data_logging_process(queue, password):
    """Fetches data and logs it, also checks and controls the socket based on house consumption."""
    while True:
        data = get_all_enpalone_data()
        if all(data.values()):
            socket_status = check_and_switch_socket(data, password)
            log_data_to_console(data, socket_status)
            data["socket_status"] = socket_status  # Update the socket status in the data
            queue.put(data)
        else:
            logger.warning("Failed to fetch all required data.")
        time.sleep(DATA_FETCH_INTERVAL)


if __name__ == "__main__":
    data_queue = Queue()

    # Start the data logging process
    logging_process = Process(
        target=data_logging_process,
        args=(
            data_queue,
            password,
        ),
    )
    logging_process.start()

    # Start the Flask app process
    from app.flask_app import run_flask_app

    flask_process = Process(target=run_flask_app, args=(data_queue,))
    flask_process.start()

    logging_process.join()
    flask_process.join()
