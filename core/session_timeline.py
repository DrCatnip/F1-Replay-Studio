class SessionTimeline:

    def __init__(self):

        self.drivers = {}

    def add_driver_data(
        self,
        driver,
        position_data
    ):

        self.drivers[driver] = position_data

    def get_driver_position(
        self,
        driver,
        frame
    ):

        if driver not in self.drivers:
            return None

        data = self.drivers[driver]

        if frame >= len(data):
            return None

        return (
            data["X"].iloc[frame],
            data["Y"].iloc[frame]
        )