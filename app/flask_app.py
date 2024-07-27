from flask import Flask, jsonify, render_template
import os
import json
from datetime import datetime, timedelta
import logging

app = Flask(__name__, template_folder="../templates")  # Adjust template folder path

# Set Flask's logger to WARNING level
app.logger.setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)


def get_latest_data():
    # Implement logic to read the most recent data file
    # This is a placeholder and needs to be implemented
    return {}


def get_historical_data(days=1):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    data = []

    base_path = os.path.join("app", "logs")
    for year in os.listdir(base_path):
        year_path = os.path.join(base_path, year)
        for month in os.listdir(year_path):
            month_path = os.path.join(year_path, month)
            for day in os.listdir(month_path):
                day_path = os.path.join(month_path, day)
                for file in os.listdir(day_path):
                    file_path = os.path.join(day_path, file)
                    file_date = datetime.strptime(file.split(".")[0], "%Y-%m-%d-%H-%M-%S")
                    if start_date <= file_date <= end_date:
                        with open(file_path, "r") as f:
                            entry = json.load(f)
                            data.append(entry)

    return sorted(data, key=lambda x: x["timestamp"])


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/data")
def get_data():
    return jsonify(get_latest_data())


@app.route("/api/historical/<int:days>")
def get_historical(days):
    return jsonify(get_historical_data(days))


def run_flask_app():
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    run_flask_app()
