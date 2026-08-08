from __future__ import annotations

from collections import deque
from contextlib import contextmanager
from time import perf_counter


class PerformanceMonitor:
    """
    Small profiler used by the replay engine.

    Example:

        profiler.begin_frame()

        with profiler.measure("cars"):
            ...

        with profiler.measure("telemetry"):
            ...

        with profiler.measure("draw"):
            ...

        profiler.end_frame()
    """

    def __init__(self, history: int = 120):

        self.history = history

        self.frame_times = deque(maxlen=history)

        self.sections = {}

        self._frame_start = None

    def begin_frame(self):

        self._frame_start = perf_counter()

    def end_frame(self):

        if self._frame_start is None:
            return

        elapsed = (perf_counter() - self._frame_start) * 1000

        self.frame_times.append(elapsed)
        self._frame_start = None

    @contextmanager
    def measure(self, name: str):

        start = perf_counter()

        yield

        elapsed = (perf_counter() - start) * 1000

        if name not in self.sections:

            self.sections[name] = deque(maxlen=self.history)

        self.sections[name].append(elapsed)

    @property
    def average_frame_time(self):

        if not self.frame_times:
            return 0.0

        return sum(self.frame_times) / len(self.frame_times)

    @property
    def fps(self):

        avg = self.average_frame_time

        if avg == 0:
            return 0

        return round(1000 / avg)

    def average(self, name):

        if name not in self.sections:
            return 0.0

        values = self.sections[name]

        if not values:
            return 0.0

        return sum(values) / len(values)

    def print_stats(self):

        print("=" * 55)
        print(f"FPS        : {self.fps}")
        print(f"Frame Time : {self.average_frame_time:.2f} ms")

        for section in sorted(self.sections):

            print(
                f"{section:12}: {self.average(section):6.2f} ms"
            )

        print("=" * 55)
