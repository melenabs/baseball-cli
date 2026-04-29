"""Team schedule fetcher."""

VALID_TEAMS = {
    "ARI", "ATL", "BAL", "BOS", "CHC", "CWS", "CIN", "CLE", "COL", "DET",
    "HOU", "KC",  "LAA", "LAD", "MIA", "MIL", "MIN", "NYM", "NYY", "OAK",
    "PHI", "PIT", "SD",  "SEA", "SF",  "STL", "TB",  "TEX", "TOR", "WSH",
}


def show_schedule(team: str) -> None:
    team = team.upper()
    if team not in VALID_TEAMS:
        raise ValueError(f"Unknown team abbreviation: '{team}'. Use standard MLB codes like NYY, LAD, BOS.")
    # TODO: implement with pybaseball / MLB Stats API
    print(f"[stub] Schedule for {team}")
