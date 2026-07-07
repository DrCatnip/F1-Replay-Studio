from __future__ import annotations

from typing import Any

import pandas as pd


class InterpolationEngine:
    """Position lookup engine preserving the existing previous-sample behavior."""

    def position_at(
        self,
        data: Any,
        timestamp: pd.Timedelta
    ) -> tuple[float, float] | None:

        rows = data[
            data["SessionTime"]
            <= timestamp
        ]

        if len(rows) == 0:
            return None

        row = rows.iloc[-1]

        return (
            row["X"],
            row["Y"]
        )
