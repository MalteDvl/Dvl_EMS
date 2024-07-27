from flask import Flask, jsonify, render_template
from multiprocessing import Queue
import logging

app = Flask(__name__, template_folder="../templates")

# Set Flask's logger to WARNING level
app.logger.setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

data_queue = None


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/live_data")
def live_data():
    if data_queue and not data_queue.empty():
        data = []
        while not data_queue.empty():
            data.append(data_queue.get())
        return jsonify(data)
    return jsonify([])


def run_flask_app(queue: Queue):
    global data_queue
    data_queue = queue
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    run_flask_app(Queue())
