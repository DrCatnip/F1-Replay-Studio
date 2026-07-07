from __future__ import annotations

from typing import Mapping

import pandas as pd


class TelemetryEngine:
    """Provides telemetry samples for the selected driver."""

    def __init__(
        self,
        telemetry_data: Mapping[str, object]
    ) -> None:

        self.telemetry_data = dict(telemetry_data)

    def sample_for_driver(
        self,
        driver: str,
        frame: int = 0
    ) -> dict[str, object] | None:

        telemetry = self.telemetry_data.get(
            driver
        )

        if telemetry is None:
            return None

        return telemetry.get_sample(
            frame
        )

    def sample_for_driver_at_time(
        self,
        driver: str,
        timestamp: pd.Timedelta
    ) -> dict[str, object] | None:
        telemetry = self.telemetry_data.get(
            driver
        )

        if telemetry is None:
            return None

        return telemetry.get_sample_at_time(
            timestamp
        )
