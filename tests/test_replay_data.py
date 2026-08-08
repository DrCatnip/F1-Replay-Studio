from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from core.replay_controller import ReplayController
from services.replay_service import PositionData


class ReplayDataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = PositionData(
            times_ms=np.array([0.0, 100.0, 200.0]),
            x=np.array([1.0, 2.0, 3.0]),
            y=np.array([4.0, 5.0, 6.0]),
        )

    def test_position_lookup_uses_previous_sample(self) -> None:
        self.assertEqual(self.data.position_at(pd.Timedelta(milliseconds=150)), (2.0, 5.0))

    def test_seek_and_speed_are_bounded(self) -> None:
        controller = ReplayController({"AAA": self.data}, pd.Timedelta(0), pd.Timedelta(milliseconds=200))
        controller.pause()
        controller.set_speed(2.0)
        controller.seek_progress(0.5)
        frame = controller.get_current_frame()
        self.assertEqual(frame.timestamp, pd.Timedelta(milliseconds=100))
        self.assertEqual(frame.speed, 2.0)
        self.assertEqual(frame.drivers[0].driver, "AAA")

