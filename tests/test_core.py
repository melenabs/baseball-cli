"""Tests for baseball-cli core logic."""

import pytest
from unittest.mock import patch, MagicMock
from src.schedule import show_schedule, VALID_TEAMS
from src.leaders import show_leaders, ALL_STATS
from src.stats import _format_hitting, _format_pitching


# --- schedule tests ---

def test_valid_team_abbreviation():
    """Valid team codes should not raise."""
    show_schedule("NYY")


def test_invalid_team_raises():
    """Unknown team codes should raise ValueError."""
    with pytest.raises(ValueError, match="Unknown team abbreviation"):
        show_schedule("XYZ")


def test_team_is_case_insensitive():
    """Team input should work regardless of case."""
    show_schedule("nyy")
    show_schedule("lad")


def test_all_30_teams_valid():
    """All 30 MLB team abbreviations should be accepted."""
    for team in VALID_TEAMS:
        show_schedule(team)


# --- leaders tests ---

def test_valid_stat():
    """Known stats should not raise."""
    show_leaders("HR")
    show_leaders("ERA")


def test_invalid_stat_raises():
    """Unknown stat should raise ValueError."""
    with pytest.raises(ValueError, match="Unknown stat"):
        show_leaders("XYZ")


def test_stat_is_case_insensitive():
    """Stat input should work regardless of case."""
    show_leaders("hr")
    show_leaders("era")


def test_top_n_param():
    """top parameter should be accepted without error."""
    show_leaders("HR", top=5)
    show_leaders("ERA", top=20)


# --- player stats formatting tests ---

def test_format_hitting_all_fields():
    """Hitting formatter should include key stat labels."""
    stats = {
        "gamesPlayed": 150, "atBats": 500, "hits": 140,
        "homeRuns": 30, "rbi": 95, "stolenBases": 10,
        "avg": ".280", "obp": ".360", "slg": ".520", "ops": ".880",
    }
    output = _format_hitting(stats)
    assert "AVG" in output
    assert "OPS" in output
    assert ".280" in output
    assert "30" in output


def test_format_hitting_missing_fields():
    """Hitting formatter should handle missing fields gracefully."""
    output = _format_hitting({})
    assert "N/A" in output


def test_format_pitching_all_fields():
    """Pitching formatter should include key stat labels."""
    stats = {
        "gamesPlayed": 32, "gamesStarted": 32, "wins": 15,
        "losses": 8, "era": "3.25", "inningsPitched": "195.0",
        "strikeOuts": 220, "baseOnBalls": 55, "whip": "1.12", "saves": 0,
    }
    output = _format_pitching(stats)
    assert "ERA" in output
    assert "3.25" in output
    assert "220" in output


def test_format_pitching_missing_fields():
    """Pitching formatter should handle missing fields gracefully."""
    output = _format_pitching({})
    assert "N/A" in output


def test_search_player_no_results_raises():
    """_search_player should raise ValueError when API returns no players."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"people": []}
    mock_resp.raise_for_status = MagicMock()

    with patch("src.stats.requests.get", return_value=mock_resp):
        from src.stats import _search_player
        with pytest.raises(ValueError, match="No player found"):
            _search_player("zzznobody")


def test_search_player_prefers_active():
    """_search_player should prefer active players over inactive ones."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "people": [
            {"id": 1, "fullName": "Old Player", "active": False},
            {"id": 2, "fullName": "Active Player", "active": True},
        ]
    }
    mock_resp.raise_for_status = MagicMock()

    with patch("src.stats.requests.get", return_value=mock_resp):
        from src.stats import _search_player
        result = _search_player("player")
        assert result["id"] == 2
