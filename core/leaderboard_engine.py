from __future__ import annotations


class LeaderboardEngine:
    """Builds the driver ordering displayed by the leaderboard."""

    def __init__(
        self,
        drivers: list[str]
    ) -> None:

        self.drivers = list(drivers)

    def current_order(self) -> list[str]:
        return list(self.drivers)
