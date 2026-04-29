"""MLB standings by division using the MLB Stats API."""

import requests

MLB_API = "https://statsapi.mlb.com/api/v1"
HEADERS = {"User-Agent": "baseball-cli/1.0"}

LEAGUE_IDS = "103,104"

DIVISION_ORDER = [
    "American League West",
    "American League Central",
    "American League East",
    "National League West",
    "National League Central",
    "National League East",
]


def _fetch_standings(season: int) -> list:
    """Fetch raw standings data from the MLB Stats API."""
    url = f"{MLB_API}/standings"
    params = {
        "leagueId": LEAGUE_IDS,
        "season": season,
        "standingsTypes": "regularSeason",
    }
    resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json().get("records", [])


def _format_division(division_name: str, teams: list) -> str:
    """Format a single division's standings as a table."""
    lines = [f"\n{division_name}"]
    lines.append(f"  {'Team':<25} {'W':>3} {'L':>3} {'PCT':>5} {'GB':>5}")
    lines.append("  " + "─" * 45)
    for team in teams:
        name = team["team"]["name"]
        w = team["wins"]
        l = team["losses"]
        pct = team["winningPercentage"]
        gb = team.get("gamesBack", "-")
        if gb == "0.0" or gb == 0:
            gb = "-"
        lines.append(f"  {name:<25} {w:>3} {l:>3} {pct:>5} {gb:>5}")
    return "\n".join(lines)


def show_standings(season: int = 2024) -> None:
    """Fetch and display MLB standings grouped by division."""
    records = _fetch_standings(season)

    divisions: dict[str, list] = {}
    for record in records:
        division_name = record.get("division", {}).get("nameShort", "")
        full_name = (
            division_name
            .replace("AL ", "American League ")
            .replace("NL ", "National League ")
        )
        divisions[full_name] = sorted(
            record.get("teamRecords", []),
            key=lambda t: float(t.get("winningPercentage", "0")),
            reverse=True,
        )

    print(f"\nMLB Standings — {season}")
    print("═" * 47)

    for div_name in DIVISION_ORDER:
        if div_name in divisions:
            print(_format_division(div_name, divisions[div_name]))

    print()
