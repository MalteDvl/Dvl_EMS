import requests
import sys
from sys import argv
from app.config import FRITZBOX_URL, FRITZBOX_AIN
from app.generate_sid import generate_sid
import logging

# Setup logger
logger = logging.getLogger("fritz_api")
logger.setLevel(logging.INFO)  # Adjust as necessary for your environment
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def switch_fritz_device(action, password):
    sid = generate_sid(password)
    if sid == "0000000000000000":
        logger.error("Failed to generate a valid SID. Check username/password.")
        return 403, "Invalid SID generated. Check username/password."

    url = f"{FRITZBOX_URL}/webservices/homeautoswitch.lua"
    params = {"ain": FRITZBOX_AIN, "switchcmd": action, "sid": sid}
    try:
        response = requests.get(url, params=params)
        return response.status_code, response.content.decode("utf-8")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error performing switch command: {e}")
        return 500, str(e)


def get_socket_state(password):
    logger.debug("Generating SID for socket state check.")
    sid = generate_sid(password)
    if sid == "0000000000000000":
        logger.error("Failed to generate valid SID.")
        return 500, "Invalid SID"

    url = f"{FRITZBOX_URL}/webservices/homeautoswitch.lua"
    params = {"ain": FRITZBOX_AIN, "switchcmd": "getswitchstate", "sid": sid}
    try:
        response = requests.get(url, params=params)
        raw_response = response.content.decode("utf-8").strip()
        logger.debug(f"Raw socket state response: {raw_response}")  # Log the raw response
        if raw_response.isdigit():
            logger.debug(f"Socket state received: {raw_response}")
            return response.status_code, raw_response
        else:
            logger.error(f"Unexpected socket state received: {raw_response}")
            return 500, "Unexpected state"
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch socket state: {e}")
        return 500, "Error fetching state"


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python fritz_api.py <password> <action>")
        sys.exit(1)
    password = argv[1]
    action = argv[2]
    status_code, response = switch_fritz_device(action, password)
    print(f"Status Code: {status_code}")
    print(f"Response: {response}")
