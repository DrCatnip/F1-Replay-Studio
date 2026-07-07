from __future__ import annotations

from typing import Any

from core.telemetry import TelemetryData


class TelemetryService:
    """Builds telemetry providers from FastF1 laps."""

    def telemetry_for_lap(
        self,
        lap: Any
    ) -> TelemetryData:

        return TelemetryData(
            lap
        )
