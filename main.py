#!/usr/bin/env python3
"""
baseball-cli — A command-line tool for MLB stats and standings.
"""

import argparse
import sys
from src import stats, standings, schedule, leaders


def build_parser():
    parser = argparse.ArgumentParser(
        prog="baseball",
        description="MLB stats at your fingertips",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # player stats
    player_p = subparsers.add_parser("player", help="Look up a player's season stats")
    player_p.add_argument("name", type=str, help='Player name, e.g. "Shohei Ohtani"')
    player_p.add_argument("--year", type=int, default=2026, help="Season year (default: 2024)")

    # standings
    subparsers.add_parser("standings", help="Current MLB standings by division")

    # schedule
    sched_p = subparsers.add_parser("schedule", help="Recent/upcoming games for a team")
    sched_p.add_argument("team", type=str, help='Team abbreviation, e.g. "NYY"')

    # leaders
    lead_p = subparsers.add_parser("leaders", help="League leaders for a stat")
    lead_p.add_argument("stat", type=str, help='Stat name, e.g. "HR", "AVG", "ERA"')
    lead_p.add_argument("--top", type=int, default=10, help="Number of results (default: 10)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "player":
            stats.show_player(args.name, args.year)
        elif args.command == "standings":
            standings.show_standings()
        elif args.command == "schedule":
            schedule.show_schedule(args.team)
        elif args.command == "leaders":
            leaders.show_leaders(args.stat, args.top)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
