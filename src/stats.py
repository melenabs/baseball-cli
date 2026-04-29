"""Player season stats lookup using the MLB Stats API."""

import requests

MLB_API = "https://statsapi.mlb.com/api/v1"
HEADERS = {"User-Agent": "baseball-cli/1.0"}


def _search_player(name: str) -> dict:
    """Search for a player by name. Returns the best match or raises."""
    url = f"{MLB_API}/people/search"
    resp = requests.get(url, params={"names": name, "sportId": 1}, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    people = resp.json().get("people", [])

    if not people:
        raise ValueError(f"No player found matching '{name}'.")

    # Prefer active MLB players; fall back to first result
    active = [p for p in people if p.get("active")]
    return active[0] if active else people[0]


def _get_hitting_stats(player_id: int, year: int) -> dict | None:
    """Fetch season hitting stats for a player."""
    url = f"{MLB_API}/people/{player_id}/stats"
    params = {"stats": "season", "group": "hitting", "season": year, "sportId": 1}
    resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    splits = resp.json().get("stats", [{}])[0].get("splits", [])
    return splits[0]["stat"] if splits else None


def _get_pitching_stats(player_id: int, year: int) -> dict | None:
    """Fetch season pitching stats for a player."""
    url = f"{MLB_API}/people/{player_id}/stats"
    params = {"stats": "season", "group": "pitching", "season": year, "sportId": 1}
    resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    splits = resp.json().get("stats", [{}])[0].get("splits", [])
    return splits[0]["stat"] if splits else None


def _format_hitting(stats: dict) -> str:
    lines = [
        f"  G:   {stats.get('gamesPlayed', 'N/A'):>6}    AB:  {stats.get('atBats', 'N/A'):>6}",
        f"  H:   {stats.get('hits', 'N/A'):>6}    HR:  {stats.get('homeRuns', 'N/A'):>6}",
        f"  RBI: {stats.get('rbi', 'N/A'):>6}    SB:  {stats.get('stolenBases', 'N/A'):>6}",
        f"  AVG: {stats.get('avg', 'N/A'):>6}    OBP: {stats.get('obp', 'N/A'):>6}",
        f"  SLG: {stats.get('slg', 'N/A'):>6}    OPS: {stats.get('ops', 'N/A'):>6}",
    ]
    return "\n".join(lines)


def _format_pitching(stats: dict) -> str:
    lines = [
        f"  G:   {stats.get('gamesPlayed', 'N/A'):>6}    GS:  {stats.get('gamesStarted', 'N/A'):>6}",
        f"  W:   {stats.get('wins', 'N/A'):>6}    L:   {stats.get('losses', 'N/A'):>6}",
        f"  ERA: {stats.get('era', 'N/A'):>6}    IP:  {stats.get('inningsPitched', 'N/A'):>6}",
        f"  SO:  {stats.get('strikeOuts', 'N/A'):>6}    BB:  {stats.get('baseOnBalls', 'N/A'):>6}",
        f"  WHIP:{stats.get('whip', 'N/A'):>6}    SV:  {stats.get('saves', 'N/A'):>6}",
    ]
    return "\n".join(lines)


def show_player(name: str, year: int) -> None:
    """Look up and display a player's season stats."""
    player = _search_player(name)
    player_id = player["id"]
    full_name = player["fullName"]
    position = player.get("primaryPosition", {}).get("abbreviation", "?")

    print(f"\n{full_name} ({position}) — {year} Season Stats")
    print("─" * 40)

    hitting = _get_hitting_stats(player_id, year)
    pitching = _get_pitching_stats(player_id, year)

    if hitting:
        print("Batting:")
        print(_format_hitting(hitting))

    if pitching:
        print("Pitching:")
        print(_format_pitching(pitching))

    if not hitting and not pitching:
        print(f"  No stats found for {year}.")
