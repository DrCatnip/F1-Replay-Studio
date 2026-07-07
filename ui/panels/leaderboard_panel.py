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
