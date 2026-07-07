class ReplayEngine:

    def __init__(self, total_frames):

        self.current_frame = 0
        self.total_frames = total_frames

        self.playing = True
        self.speed = 1

    def update(self):

        if not self.playing:
            return

        self.current_frame += self.speed

        if self.current_frame >= self.total_frames:
            self.current_frame = 0

    def get_frame(self):

        return int(self.current_frame)

    def toggle_play(self):

        self.playing = not self.playing

        if self.playing:
            print("PLAY")
        else:
            print("PAUSE")

    def set_speed(self, speed):

        self.speed = speed

        print(f"Speed set to {speed}x")