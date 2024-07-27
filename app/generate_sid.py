# generate_sid.py
import requests
import hashlib
from app.config import FRITZBOX_URL, FRITZBOX_USERNAME


def generate_sid(password):
    url = f"{FRITZBOX_URL}/login_sid.lua"
    response = requests.get(url)
    data = response.content.decode("utf-8")
    challenge = data.split("<Challenge>")[1].split("</Challenge>")[0]

    to_hash = f"{challenge}-{password}".encode("utf-16le")
    md5_hash = hashlib.md5(to_hash)
    response_hash = f"{challenge}-{md5_hash.hexdigest()}"

    params = {"username": FRITZBOX_USERNAME, "response": response_hash}
    response = requests.get(url, params=params)
    sid = response.content.decode("utf-8").split("<SID>")[1].split("</SID>")[0]
    return sid
