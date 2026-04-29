"""Team schedule fetcher using the MLB Stats API."""

import requests
from datetime import date, timedelta

MLB_API = "https://statsapi.mlb.com/api/v1"
HEADERS = {"User-Agent": "baseball-cli/1.0"}

VALID_TEAMS = {
    "ARI", "ATL", "BAL", "BOS", "CHC", "CWS", "CIN", "CLE", "COL", "DET",
    "HOU", "KC",  "LAA", "LAD", "MIA", "MIL", "MIN", "NYM", "NYY", "OAK",
    "PHI", "PIT", "SD",  "SEA", "SF",  "STL", "TB",  "TEX", "TOR", "WSH",
}

TEAM_IDS = {
    "ARI": 109, "ATL": 144, "BAL": 110, "BOS": 111, "CHC": 112,
    "CWS": 145, "CIN": 113, "CLE": 114, "COL": 115, "DET": 116,
    "HOU": 117, "KC":  118, "LAA": 108, "LAD": 119, "MIA": 146,
    "MIL": 158, "MIN": 142, "NYM": 121, "NYY": 147, "OAK": 133,
    "PHI": 143, "PIT": 134, "SD":  135, "SEA": 136, "SF":  137,
    "STL": 138, "TB":  139, "TEX": 140, "TOR": 141, "WSH": 120,
}


def _fetch_schedule(team_id: int, start_date: str, end_date: str) -> list:
    """Fetch schedule for a team between two dates."""
    url = f"{MLB_API}/schedule"
    params = {
        "teamId": team_id,
        "startDate": start_date,
        "endDate": end_date,
        "sportId": 1,
        "hydrate": "team",
    }
    resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json().get("dates", [])


def _format_game(game: dict, team_abbr: str) -> str:
    """Format a single game into a readable line."""
    teams = game.get("teams", {})
    away = teams.get("away", {}).get("team", {}).get("name", "?")
    home = teams.get("home", {}).get("team", {}).get("name", "?")
    status = game.get("status", {}).get("detailedState", "?")
    game_time = game.get("gameDate", "")[:10]  # YYYY-MM-DD

    away_score = teams.get("away", {}).get("score")
    home_score = teams.get("home", {}).get("score")

    if status == "Final" and away_score is not None:
        score = f"{away_score}-{home_score}"
        return f"  {game_time}  {away:<25} @ {home:<25} Final: {score}"
    elif status in ("In Progress", "Live"):
        score = f"{away_score}-{home_score}"
        return f"  {game_time}  {away:<25} @ {home:<25} LIVE: {score}"
    else:
        game_time_str = game.get("gameDate", "")[11:16]  # HH:MM UTC
        return f"  {game_time}  {away:<25} @ {home:<25} {game_time_str} UTC"


def show_schedule(team: str) -> None:
    """Show the last 3 days and next 7 days of games for a team."""
    team = team.upper()
    if team not in VALID_TEAMS:
        raise ValueError(
            f"Unknown team abbreviation: '{team}'. "
            f"Use standard MLB codes like NYY, LAD, BOS."
        )

    team_id = TEAM_IDS[team]
    today = date.today()
    start = (today - timedelta(days=3)).strftime("%Y-%m-%d")
    end = (today + timedelta(days=7)).strftime("%Y-%m-%d")

    dates = _fetch_schedule(team_id, start, end)

    print(f"\n{team} Schedule — {start} to {end}")
    print("═" * 70)

    if not dates:
        print("  No games found in this window.")
        print()
        return

    for date_entry in dates:
        for game in date_entry.get("games", []):
            print(_format_game(game, team))

    print()
