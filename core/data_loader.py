import fastf1

fastf1.Cache.enable_cache("cache")


def load_session(
    year,
    grand_prix,
    session_type
):
    session = fastf1.get_session(
        year,
        grand_prix,
        session_type
    )

    session.load()

    return session