"""Command-line interface for the HazardWatch prototype."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

from .pipeline import run_pipeline
from .stac_search import DEFAULT_STAC_URL, SENTINEL_COLLECTIONS

CLI_VERSION = "0.1.0"
DEFAULT_PLAN_STEPS = [
    "Validate AOI geometry and date/date-range input",
    "Search STAC for Sentinel-1 and Sentinel-2 scenes",
    "Rank scenes by acquisition datetime",
    "Emit a concise result table or machine-readable JSON",
]

IMH_BANNER = r"""
╔════════════════════════════════════════════════════════════╗
║      ██╗███╗   ███╗██╗  ██╗   InstaHazard Maps CLI       ║
║      ██║████╗ ████║██║  ██║   Rapid disaster mapping      ║
║      ██║██╔████╔██║███████║   Sentinel scene discovery    ║
║      ██║██║╚██╔╝██║██╔══██║   Stay ready. Move fast.      ║
║      ██║██║ ╚═╝ ██║██║  ██║                               ║
║      ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝                               ║
╚════════════════════════════════════════════════════════════╝
""".strip("\n")


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level CLI parser."""
    parser = argparse.ArgumentParser(
        prog="hazardwatch",
        description="Codex-style disaster mapping CLI for rapid Sentinel scene discovery.",
    )
    parser.add_argument(
        "--stac-url",
        default=DEFAULT_STAC_URL,
        help="STAC API endpoint to query (default: Planetary Computer)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {CLI_VERSION}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser(
        "search",
        help="Search for scenes over an AOI and date/date range.",
    )
    search_parser.add_argument("aoi", help="Path to AOI GeoJSON file")
    search_parser.add_argument("date", help="ISO date or date range (YYYY-MM-DD/YYYY-MM-DD)")
    search_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of results to print",
    )
    search_parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output",
    )

    sources_parser = subparsers.add_parser(
        "sources",
        help="Show configured imagery sources and STAC endpoint.",
    )
    sources_parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output",
    )

    plan_parser = subparsers.add_parser(
        "plan",
        help="Show planned workflow stages for the current HazardWatch CLI.",
    )
    plan_parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output",
    )

    return parser


def _summarize_item(item: Any) -> Dict[str, Any]:
    item_id = getattr(item, "id", None)
    collection_id = getattr(item, "collection_id", None)
    properties = getattr(item, "properties", {}) or {}

    if item_id is None and isinstance(item, dict):
        item_id = item.get("id")
        properties = item.get("properties", properties)
        collection_id = item.get("collection") or item.get("collection_id")

    return {
        "id": item_id,
        "collection": collection_id,
        "datetime": properties.get("datetime"),
    }


def cmd_search(args: argparse.Namespace) -> int:
    items = run_pipeline(args.aoi, args.date, stac_url=args.stac_url)
    summaries: List[Dict[str, Any]] = [_summarize_item(item) for item in items[: args.limit]]

    if args.json:
        print(
            json.dumps(
                {
                    "count": len(items),
                    "showing": len(summaries),
                    "results": summaries,
                },
                indent=2,
            )
        )
    else:
        print(f"Found {len(items)} scene(s); showing {len(summaries)}")
        for idx, summary in enumerate(summaries, start=1):
            print(
                f"{idx}. {summary.get('id')} "
                f"[{summary.get('collection')}] "
                f"{summary.get('datetime')}"
            )

    return 0


def cmd_sources(args: argparse.Namespace) -> int:
    payload = {
        "stac_url": args.stac_url,
        "collections": SENTINEL_COLLECTIONS,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"STAC endpoint: {payload['stac_url']}")
        print("Collections:")
        for collection in payload["collections"]:
            print(f"- {collection}")

    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    payload = {
        "workflow": "scene-discovery",
        "steps": DEFAULT_PLAN_STEPS,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print("HazardWatch CLI workflow plan:")
        for idx, step in enumerate(payload["steps"], start=1):
            print(f"{idx}. {step}")

    return 0


def should_show_banner(args: argparse.Namespace) -> bool:
    """Return True when the terminal banner should be printed."""
    if os.getenv("HAZARDWATCH_NO_BANNER"):
        return False

    if getattr(args, "json", False):
        return False

    return sys.stdout.isatty()


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if should_show_banner(args):
        print(IMH_BANNER)

    if args.command == "search":
        return cmd_search(args)

    if args.command == "sources":
        return cmd_sources(args)

    if args.command == "plan":
        return cmd_plan(args)

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
