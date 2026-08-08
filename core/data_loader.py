"""Legacy compatibility entry point.

New code should use :class:`core.session_loader.SessionLoader`; this helper
keeps older integrations on the same FastF1 service and cache boundary.
"""

from services.fastf1_service import FastF1Service


def load_session(
    year,
    grand_prix,
    session_type
):
    return FastF1Service().load_session(year, grand_prix, session_type)
