# baseball-cli

A command-line tool for live MLB stats, standings, schedules, and league leaders. Built with Python using the MLB Stats API — no API key required.

## Installation

**Requirements:** Python 3.10+

```bash
git clone https://github.com/melenabs/baseball-cli.git
cd baseball-cli
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py <command> [options]
```

## Commands

### `player` — Look up a player's season stats

```bash
python3 main.py player "Shohei Ohtani"
python3 main.py player "Gerrit Cole"
python3 main.py player "Aaron Judge" --year 2025
```

**Expected output:**
```
Shohei Ohtani (DH) — 2026 Season Stats
────────────────────────────────────────
Batting:
  G:      45    AB:     160
  H:      48    HR:      12
  RBI:    35    SB:       5
  AVG:  .300    OBP:  .385
  SLG:  .560    OPS:  .945
```

---

### `standings` — Current MLB standings by division

```bash
python3 main.py standings
python3 main.py standings --year 2025
```

**Expected output:**
```
MLB Standings — 2026
═══════════════════════════════════════════════

American League East
  Team                       W   L   PCT    GB
  ─────────────────────────────────────────────
  New York Yankees          22   9  .710     -
  Baltimore Orioles         18  13  .581   4.0
  ...
```

---

### `leaders` — League leaders for a stat

```bash
python3 main.py leaders HR
python3 main.py leaders AVG --top 5
python3 main.py leaders ERA --top 15
```

Available stats:
- **Batting:** HR, AVG, RBI, OBP, SLG, OPS, SB, H, R
- **Pitching:** ERA, SO, W, WHIP, SV, IP

**Expected output:**
```
MLB Batting Leaders — Home Runs (2026)
═══════════════════════════════════════
  #    Player                    Team                  HR
  ──────────────────────────────────────────────────────
  1    Aaron Judge               New York Yankees       14
  2    Kyle Schwarber            Philadelphia Phillies  13
  ...
```

---

### `schedule` — Recent and upcoming games for a team

```bash
python3 main.py schedule NYY
python3 main.py schedule LAD
python3 main.py schedule BOS
```

Uses standard MLB team abbreviations (NYY, LAD, BOS, CHC, etc.). Shows the last 3 days and next 7 days.

**Expected output:**
```
NYY Schedule — 2026-04-25 to 2026-05-05
══════════════════════════════════════════════════════════════════════
  2026-04-26  Boston Red Sox            @ New York Yankees      Final: 3-5
  2026-04-27  Boston Red Sox            @ New York Yankees      Final: 7-2
  2026-04-28  Toronto Blue Jays         @ New York Yankees      19:05 UTC
```

---

## Running Tests

```bash
pytest
```

All tests use mocked API responses so they run offline and fast.

## Known Limitations

- `player` search works best with full names (e.g. `"Shohei Ohtani"` not `"ohtani"`)
- Schedule times are displayed in UTC
- Stats data depends on MLB Stats API availability

## Future Ideas

- `compare` command for head-to-head player stats
- `--json` flag for machine-readable output
- Career stats with `--career` flag
