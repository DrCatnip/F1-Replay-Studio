from __future__ import annotations

import unittest

from core.performance_monitor import PerformanceMonitor


class PerformanceMonitorTests(unittest.TestCase):
    def test_records_frame_and_named_section(self) -> None:
        monitor = PerformanceMonitor(history=2)
        monitor.begin_frame()
        with monitor.measure("render"):
            pass
        monitor.end_frame()
        self.assertGreaterEqual(monitor.average_frame_time, 0)
        self.assertGreaterEqual(monitor.average("render"), 0)
        self.assertGreaterEqual(monitor.fps, 0)
