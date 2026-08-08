from dataclasses import dataclass
import os

from app.constants import CACHE_FOLDER, DEFAULT_EVENT, DEFAULT_SESSION, DEFAULT_YEAR


@dataclass(frozen=True)
class SessionSettings:
    year: int = DEFAULT_YEAR
    event: str = DEFAULT_EVENT
    session_type: str = DEFAULT_SESSION


@dataclass(frozen=True)
class ApplicationSettings:
    cache_folder: str = os.environ.get("F1_REPLAY_CACHE", CACHE_FOLDER)
    default_session: SessionSettings = SessionSettings()
    debug_performance: bool = os.environ.get("F1_REPLAY_DEBUG_PERFORMANCE", "").lower() in {"1", "true", "yes"}
