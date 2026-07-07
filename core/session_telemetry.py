import pandas as pd


class SessionTelemetry:

    def __init__(self):

        self.drivers = {}

    def add_driver(
        self,
        driver,
        car_data
    ):

        self.drivers[driver] = car_data

    def get_sample(
        self,
        driver,
        session_time
    ):

        if driver not in self.drivers:
            return None

        data = self.drivers[driver]

        rows = data[
            data["SessionTime"] <= session_time
        ]

        if len(rows) == 0:
            return None

        row = rows.iloc[-1]

        return {
            "speed": row["Speed"],
            "gear": row["nGear"],
            "throttle": row["Throttle"],
            "brake": row["Brake"]
        }