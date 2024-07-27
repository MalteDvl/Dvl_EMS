# Enpal.One Configuration
ENPALONE_URL = "http://192.168.10.24"
ENPALONE_ENDPOINTS = {
    "pv_production": "/api/pv/data/Power.DC.Total",
    "house_consumption": "/api/pv/data/Power.House.Total",
    "battery_power": "/api/pv/data/Power.Battery.Charge.Discharge",
    "grid_power": "/api/pv/data/Power.Grid.Export",
    "battery_level": "/api/pv/data/Energy.Battery.Charge.Level",
}
ENPALONE_HEADERS = {"accept": "application/json", "Signature": "123"}

# Application Configuration
DATA_FETCH_INTERVAL = 60  # seconds

# Fritz Power Socket
FRITZBOX_URL = "http://fritz.box/"
FRITZBOX_USERNAME = "fritz8584"
FRITZBOX_AIN = "116300435106"
