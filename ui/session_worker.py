from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal

from core.session_loader import SessionLoader
from services.fastf1_service import FastF1Service
from services.session_service import SessionService


class SessionWorker(QObject):
    """Runs provider work off the Qt GUI thread."""

    events_ready = pyqtSignal(int, object)
    sessions_ready = pyqtSignal(int, str, object)
    session_loaded = pyqtSignal(object)
    failed = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, cache_path: str = "cache") -> None:
        super().__init__()
        self.cache_path = cache_path

    def _session_service(self) -> SessionService:
        return SessionService(FastF1Service(self.cache_path))

    def discover_events(self, year: int) -> None:
        try:
            self.events_ready.emit(year, self._session_service().available_events(year))
        except Exception as error:
            self.failed.emit(_friendly_error(error))
        finally:
            self.finished.emit()

    def discover_sessions(self, year: int, event: str) -> None:
        try:
            self.sessions_ready.emit(year, event, self._session_service().available_sessions(year, event))
        except Exception as error:
            self.failed.emit(_friendly_error(error))
        finally:
            self.finished.emit()

    def load_session(self, year: int, event: str, session_type: str) -> None:
        try:
            self.session_loaded.emit(SessionLoader(
                cache_path=self.cache_path, year=year, event=event, session_type=session_type
            ).load())
        except Exception as error:
            self.failed.emit(_friendly_error(error))
        finally:
            self.finished.emit()


def _friendly_error(error: Exception) -> str:
    message = str(error).strip()
    if not message:
        return "Session data unavailable"
    return f"Session data unavailable: {message}"
