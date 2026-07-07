import pandas as pd


class SessionReplay:

    def __init__(self):

        self.drivers = {}

        self.current_time = None

        self.min_time = None

        self.max_time = pd.Timedelta(
            seconds=0
        )

    def add_driver(
        self,
        driver,
        pos_data
    ):

        self.drivers[
            driver
        ] = pos_data

        driver_min = (
            pos_data["SessionTime"]
            .min()
        )

        driver_max = (
            pos_data["SessionTime"]
            .max()
        )

        if (
            self.min_time is None
            or driver_min > self.min_time
        ):
            self.min_time = driver_min

        if (
            driver_max > self.max_time
        ):
            self.max_time = driver_max

    def initialize(self):

        self.current_time = (
            self.min_time
        )

    def advance(
        self,
        milliseconds=100
    ):

        self.current_time += (
            pd.Timedelta(
                milliseconds=milliseconds
            )
        )

        if (
            self.current_time
            > self.max_time
        ):

            self.current_time = (
                self.min_time
            )

    def get_position(
        self,
        driver
    ):

        if driver not in self.drivers:

            return None

        data = self.drivers[
            driver
        ]

        rows = data[
            data["SessionTime"]
            <= self.current_time
        ]

        if len(rows) == 0:

            return None

        row = rows.iloc[-1]

        return (
            row["X"],
            row["Y"]
        )