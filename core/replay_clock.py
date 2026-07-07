import pandas as pd


class ReplayClock:

    def __init__(self):

        self.current_time = None

        self.start_time = None

        self.end_time = None

        self.speed = 1

        self.playing = True

    def initialize(
        self,
        start_time,
        end_time
    ):

        self.start_time = start_time

        self.end_time = end_time

        self.current_time = start_time

    def play(self):

        self.playing = True

    def pause(self):

        self.playing = False

    def set_speed(
        self,
        speed
    ):

        self.speed = speed

    def update(self):

        if not self.playing:

            return

        self.current_time += pd.Timedelta(
            milliseconds=100 * self.speed
        )

        if self.current_time > self.end_time:

            self.current_time = self.start_time