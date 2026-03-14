"""Command-line interface for the HazardWatch prototype."""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List

from .pipeline import run_pipeline
from .stac_search import DEFAULT_STAC_URL


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


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "search":
        return cmd_search(args)

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
