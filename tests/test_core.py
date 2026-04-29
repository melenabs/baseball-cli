"""Tests for baseball-cli core logic."""

import pytest
from unittest.mock import patch, MagicMock
from src.schedule import show_schedule, VALID_TEAMS
from src.leaders import show_leaders, ALL_STATS
from src.stats import _format_hitting, _format_pitching


# --- schedule tests ---

def test_valid_team_abbreviation():
    show_schedule("NYY")

def test_invalid_team_raises():
    with pytest.raises(ValueError, match="Unknown team abbreviation"):
        show_schedule("XYZ")

def test_team_is_case_insensitive():
    show_schedule("nyy")
    show_schedule("lad")

def test_all_30_teams_valid():
    for team in VALID_TEAMS:
        show_schedule(team)


# --- leaders tests ---

def _mock_leaders_response(value="30"):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "leagueLeaders": [{
            "leaders": [{
                "rank": 1,
                "person": {"fullName": "Test Player"},
                "team": {"name": "Test Team"},
                "value": value,
            }]
        }]
    }
    mock_resp.raise_for_status = MagicMock()
    return mock_resp


def test_valid_stat():
    with patch("src.leaders.requests.get", return_value=_mock_leaders_response()):
        show_leaders("HR")
        show_leaders("ERA")

def test_invalid_stat_raises():
    with pytest.raises(ValueError, match="Unknown stat"):
        show_leaders("XYZ")

def test_stat_is_case_insensitive():
    with patch("src.leaders.requests.get", return_value=_mock_leaders_response()):
        show_leaders("hr")
        show_leaders("era")

def test_top_n_param():
    with patch("src.leaders.requests.get", return_value=_mock_leaders_response()):
        show_leaders("HR", top=5)
        show_leaders("ERA", top=20)

def test_fetch_leaders_calls_correct_url():
    from src.leaders import _fetch_leaders
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"leagueLeaders": [{"leaders": []}]}
    mock_resp.raise_for_status = MagicMock()
    with patch("src.leaders.requests.get", return_value=mock_resp) as mock_get:
        result = _fetch_leaders("HR", 2026, 10)
        assert result == []
        assert "leaders" in mock_get.call_args[0][0]

def test_fetch_leaders_empty_response():
    from src.leaders import _fetch_leaders
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"leagueLeaders": []}
    mock_resp.raise_for_status = MagicMock()
    with patch("src.leaders.requests.get", return_value=mock_resp):
        assert _fetch_leaders("ERA", 2026, 10) == []

def test_show_leaders_formats_output(capsys):
    with patch("src.leaders.requests.get", return_value=_mock_leaders_response("58")):
        show_leaders("HR", top=1)
    captured = capsys.readouterr()
    assert "Test Player" in captured.out
    assert "58" in captured.out


# --- player stats formatting tests ---

def test_format_hitting_all_fields():
    stats = {
        "gamesPlayed": 150, "atBats": 500, "hits": 140,
        "homeRuns": 30, "rbi": 95, "stolenBases": 10,
        "avg": ".280", "obp": ".360", "slg": ".520", "ops": ".880",
    }
    output = _format_hitting(stats)
    assert "AVG" in output and ".280" in output and "30" in output

def test_format_hitting_missing_fields():
    assert "N/A" in _format_hitting({})

def test_format_pitching_all_fields():
    stats = {
        "gamesPlayed": 32, "gamesStarted": 32, "wins": 15,
        "losses": 8, "era": "3.25", "inningsPitched": "195.0",
        "strikeOuts": 220, "baseOnBalls": 55, "whip": "1.12", "saves": 0,
    }
    output = _format_pitching(stats)
    assert "ERA" in output and "3.25" in output

def test_format_pitching_missing_fields():
    assert "N/A" in _format_pitching({})

def test_search_player_no_results_raises():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"people": []}
    mock_resp.raise_for_status = MagicMock()
    with patch("src.stats.requests.get", return_value=mock_resp):
        from src.stats import _search_player
        with pytest.raises(ValueError, match="No player found"):
            _search_player("zzznobody")

def test_search_player_prefers_active():
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
        assert _search_player("player")["id"] == 2


# --- standings tests ---

def test_format_division_output():
    from src.standings import _format_division
    teams = [
        {"team": {"name": "New York Yankees"}, "wins": 90, "losses": 60,
         "winningPercentage": ".600", "gamesBack": "0.0"},
        {"team": {"name": "Boston Red Sox"}, "wins": 80, "losses": 70,
         "winningPercentage": ".533", "gamesBack": "10.0"},
    ]
    output = _format_division("AL East", teams)
    assert "New York Yankees" in output and "90" in output

def test_format_division_first_place_shows_dash():
    from src.standings import _format_division
    teams = [{"team": {"name": "LA Dodgers"}, "wins": 95, "losses": 55,
              "winningPercentage": ".633", "gamesBack": "0.0"}]
    assert "-" in _format_division("NL West", teams)

def test_fetch_standings_calls_correct_url():
    from src.standings import _fetch_standings
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"records": []}
    mock_resp.raise_for_status = MagicMock()
    with patch("src.standings.requests.get", return_value=mock_resp) as mock_get:
        assert _fetch_standings(2026) == []
        assert "standings" in mock_get.call_args[0][0]
