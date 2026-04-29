"""League leaders for a given stat."""

BATTING_STATS = {"HR", "AVG", "RBI", "OBP", "SLG", "OPS", "SB", "H", "R"}
PITCHING_STATS = {"ERA", "SO", "W", "WHIP", "SV", "IP"}
ALL_STATS = BATTING_STATS | PITCHING_STATS


def show_leaders(stat: str, top: int = 10) -> None:
    stat = stat.upper()
    if stat not in ALL_STATS:
        raise ValueError(
            f"Unknown stat: '{stat}'. "
            f"Batting: {sorted(BATTING_STATS)}. "
            f"Pitching: {sorted(PITCHING_STATS)}."
        )
    # TODO: implement with pybaseball
    print(f"[stub] Top {top} leaders in {stat}")
