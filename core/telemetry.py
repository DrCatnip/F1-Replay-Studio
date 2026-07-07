from __future__ import annotations

import pandas as pd


class TelemetryData:

    def __init__(self, lap):

        self.car_data = lap.get_car_data()

    def get_sample(self, frame):

        if frame >= len(self.car_data):
            frame = len(self.car_data) - 1

        row = self.car_data.iloc[frame]

        return {
            "speed": row["Speed"],
            "gear": row["nGear"],
            "throttle": row["Throttle"],
            "brake": row["Brake"],
            "rpm": row.get("RPM", None),
            "drs": row.get("DRS", "--")
        }

    def get_sample_at_time(
        self,
        timestamp: pd.Timedelta
    ) -> dict[str, object] | None:
        if len(self.car_data) == 0:
            return None

        if "SessionTime" not in self.car_data:
            return self.get_sample(0)

        rows = self.car_data[
            self.car_data["SessionTime"]
            <= timestamp
        ]

        if len(rows) == 0:
            row = self.car_data.iloc[0]
        else:
            row = rows.iloc[-1]

        return {
            "speed": row["Speed"],
            "gear": row["nGear"],
            "throttle": row["Throttle"],
            "brake": row["Brake"],
            "rpm": row.get("RPM", None),
            "drs": row.get("DRS", "--")
        }
