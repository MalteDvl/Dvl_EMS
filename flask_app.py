from flask import Flask, jsonify, render_template
import threading
import time
from app.enpalone_api import get_all_enpalone_data
from app.config import DATA_FETCH_INTERVAL

app = Flask(__name__)

# Global variable to store the latest data
latest_data = {}


def update_data():
    global latest_data
    while True:
        try:
            data = get_all_enpalone_data()
            if all(v is not None for v in data.values()):
                latest_data = data
            time.sleep(DATA_FETCH_INTERVAL)
        except Exception as e:
            print(f"An error occurred: {str(e)}")


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/data")
def get_data():
    return jsonify(latest_data)


if __name__ == "__main__":
    # Start the data update thread
    data_thread = threading.Thread(target=update_data)
    data_thread.start()

    # Run the Flask app
    app.run(debug=True, use_reloader=False)
