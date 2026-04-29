"""MLB standings by division using the MLB Stats API."""

import requests

MLB_API = "https://statsapi.mlb.com/api/v1"
HEADERS = {"User-Agent": "baseball-cli/1.0"}

LEAGUE_IDS = "103,104"

DIVISION_ORDER = [
    "AL West",
    "AL Central",
    "AL East",
    "NL West",
    "NL Central",
    "NL East",
]

DISPLAY_NAMES = {
    "AL West": "American League West",
    "AL Central": "American League Central",
    "AL East": "American League East",
    "NL West": "National League West",
    "NL Central": "National League Central",
    "NL East": "National League East",
}


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
    display = DISPLAY_NAMES.get(division_name, division_name)
    lines = [f"\n{display}"]
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


def show_standings(season: int = 2026) -> None:
    """Fetch and display MLB standings grouped by division."""
    records = _fetch_standings(season)

    divisions: dict[str, list] = {}
    for record in records:
        # Try both short name formats the API might return
        div = record.get("division", {})
        division_name = div.get("nameShort") or div.get("name", "")
        divisions[division_name] = sorted(
            record.get("teamRecords", []),
            key=lambda t: float(t.get("winningPercentage", "0")),
            reverse=True,
        )

    print(f"\nMLB Standings — {season}")
    print("═" * 47)

    # Try to print in preferred order, then fall back to whatever came back
    printed = set()
    for div_name in DIVISION_ORDER:
        if div_name in divisions:
            print(_format_division(div_name, divisions[div_name]))
            printed.add(div_name)

    # Print any divisions not in our ordered list
    for div_name, teams in divisions.items():
        if div_name not in printed:
            print(_format_division(div_name, teams))

    print()
