from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.widgets.common.panel import Panel
from ui.widgets.common.panel_header import PanelHeader


class LeaderboardPanel(QWidget):
    """Compact leaderboard panel for the current session ordering."""

    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.panel = Panel()
        self.panel.addWidget(PanelHeader("Leaderboard"))

        self.labels: list[QLabel] = []

        for position in range(20):
            label = QLabel(f"{position + 1:02d}  --")
            self.labels.append(label)
            self.panel.addWidget(label)

        self.panel.addStretch()
        root.addWidget(self.panel)

    def update_drivers(
        self,
        drivers: list[str]
    ) -> None:
        for position, label in enumerate(self.labels):
            if position < len(drivers):
                label.setText(f"{position + 1:02d}  {drivers[position]}")
            else:
                label.setText(f"{position + 1:02d}  --")

    def update_rows(self, rows: list[dict[str, object]], selected_driver: str = "") -> None:
        if not rows:
            return self.update_drivers([])
        for index, label in enumerate(self.labels):
            if index >= len(rows):
                label.setText(f"{index + 1:02d}  --")
                continue
            row = rows[index]
            driver = str(row.get("driver", "—"))
            position = row.get("position") or index + 1
            team = str(row.get("team", "—"))
            gap = _format_gap(row.get("gap"))
            label.setText(f"{position:>2}  {driver:<3}  {team}  {gap}")
            label.setProperty("selected", driver == selected_driver)
            label.style().unpolish(label)
            label.style().polish(label)


def _format_gap(value: object) -> str:
    if value is None or str(value) in {"NaT", "nan"}:
        return "—"
    return str(value).replace("0 days ", "")
