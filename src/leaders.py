"""League leaders for a given stat using the MLB Stats API."""

import requests

MLB_API = "https://statsapi.mlb.com/api/v1"
HEADERS = {"User-Agent": "baseball-cli/1.0"}

BATTING_STATS = {"HR", "AVG", "RBI", "OBP", "SLG", "OPS", "SB", "H", "R"}
PITCHING_STATS = {"ERA", "SO", "W", "WHIP", "SV", "IP"}
ALL_STATS = BATTING_STATS | PITCHING_STATS

# Mapping CLI stat names to MLB Stats API statistic names
STAT_MAP = {
    "HR":   "homeRuns",
    "AVG":  "battingAverage",
    "RBI":  "runsBattedIn",
    "OBP":  "onBasePercentage",
    "SLG":  "sluggingPercentage",
    "OPS":  "onBasePlusSlugging",
    "SB":   "stolenBases",
    "H":    "hits",
    "R":    "runs",
    "ERA":  "earnedRunAverage",
    "SO":   "strikeouts",
    "W":    "wins",
    "WHIP": "walksAndHitsPerInningPitched",
    "SV":   "saves",
    "IP":   "inningsPitched",
}


def _fetch_leaders(stat: str, season: int, limit: int) -> list:
    """Fetch league leaders from the MLB Stats API."""
    api_stat = STAT_MAP[stat]
    url = f"{MLB_API}/stats/leaders"
    params = {
        "leaderCategories": api_stat,
        "season": season,
        "sportId": 1,
        "limit": limit,
    }
    resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    categories = resp.json().get("leagueLeaders", [])
    return categories[0].get("leaders", []) if categories else []


def show_leaders(stat: str, top: int = 10, season: int = 2026) -> None:
    """Display league leaders for a given stat."""
    stat = stat.upper()
    if stat not in ALL_STATS:
        raise ValueError(
            f"Unknown stat: '{stat}'. "
            f"Batting: {sorted(BATTING_STATS)}. "
            f"Pitching: {sorted(PITCHING_STATS)}."
        )

    leaders = _fetch_leaders(stat, season, top)

    print(f"\nMLB Leaders — {stat} ({season})")
    print("═" * 40)
    print(f"  {'#':<4} {'Player':<25} {'Team':<20} {stat:>6}")
    print("  " + "─" * 58)

    for entry in leaders:
        rank = entry.get("rank", "?")
        name = entry.get("person", {}).get("fullName", "Unknown")
        team = entry.get("team", {}).get("name", "N/A")
        value = entry.get("value", "N/A")
        print(f"  {rank:<4} {name:<25} {team:<20} {value:>6}")

    print()
