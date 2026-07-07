import matplotlib.pyplot as plt


TEAM_COLORS = {
    "LEC": "red",
    "SAI": "red",

    "VER": "blue",
    "PER": "blue",

    "NOR": "orange",
    "PIA": "orange",

    "HAM": "cyan",
    "RUS": "cyan"
}


class TrackRenderer:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        plt.ion()

        self.fig, self.ax = plt.subplots(
            figsize=(8, 8)
        )

        self.ax.plot(
            self.x,
            self.y,
            alpha=0.3
        )

        self.ax.set_aspect("equal")

        self.cars = {}
        self.labels = {}

    def add_driver(
        self,
        driver
    ):

        color = TEAM_COLORS.get(
            driver,
            "black"
        )

        car, = self.ax.plot(
            [],
            [],
            "o",
            markersize=8,
            color=color
        )

        label = self.ax.text(
            0,
            0,
            driver,
            fontsize=8,
            color=color
        )

        self.cars[driver] = car
        self.labels[driver] = label

    def draw_driver(
        self,
        driver,
        x,
        y
    ):

        self.cars[driver].set_data(
            [x],
            [y]
        )

        self.labels[driver].set_position(
            (x + 20, y + 20)
        )

        plt.pause(0.001)