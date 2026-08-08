from __future__ import annotations

import unittest

import pandas as pd

from services.session_service import SessionService


class FakeFastF1Service:
    def event_schedule(self, _year: int):
        return pd.DataFrame([{
            "EventName": "Example Grand Prix", "RoundNumber": 2,
            "EventDate": pd.Timestamp("2026-03-15"),
            "Session1": "Practice 1", "Session2": "Practice 2",
            "Session3": "Practice 3", "Session4": "Qualifying", "Session5": "Race",
        }])


class SessionServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SessionService(FakeFastF1Service())

    def test_events_are_provider_driven(self) -> None:
        events = self.service.available_events(2026)
        self.assertEqual(events[0].name, "Example Grand Prix")
        self.assertEqual(events[0].round_number, 2)

    def test_sessions_are_provider_driven(self) -> None:
        sessions = self.service.available_sessions(2026, "Example Grand Prix")
        self.assertEqual([(item.name, item.code) for item in sessions][-2:], [("Qualifying", "Q"), ("Race", "R")])

