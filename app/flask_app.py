from flask import Flask, jsonify, render_template
from queue import Queue, Empty
import logging

app = Flask(__name__, template_folder="../templates")

# Set up a logger
logger = logging.getLogger("flask_app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

data_queue = None
last_data_snapshot = None  # Store the last valid data snapshot


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/live_data")
def live_data():
    global last_data_snapshot
    if last_data_snapshot:
        return jsonify(last_data_snapshot)
    return jsonify([])


@app.route("/api/socket_status")
def socket_status():
    if last_data_snapshot:
        return jsonify({"status": last_data_snapshot.get("socket_status", "0")})
    return jsonify({"status": "0"})


def run_flask_app(queue: Queue):
    global data_queue, last_data_snapshot
    data_queue = queue
    while True:
        try:
            data = data_queue.get_nowait()  # Non-blocking get
            last_data_snapshot = data  # Update the snapshot
        except Empty:
            pass
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    run_flask_app(Queue())
