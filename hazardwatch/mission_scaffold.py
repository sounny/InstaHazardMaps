"""CLI scaffolding for first-responder hazard mapping missions.

This module helps teams turn incident details into a structured mission packet
and a reusable Codex CLI prompt.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import List


@dataclass
class MissionPacket:
    """Structured information needed to run a first-response mapping mission."""

    incident_name: str
    hazard_type: str
    location: str
    date_range: str
    priority_layers: List[str]
    requester: str
    notes: str = ""


def create_mission_packet(
    incident_name: str,
    hazard_type: str,
    location: str,
    date_range: str,
    priority_layers: List[str],
    requester: str,
    notes: str = "",
) -> MissionPacket:
    """Create a mission packet with normalized text fields."""

    normalized_layers = [layer.strip() for layer in priority_layers if layer.strip()]
    if not normalized_layers:
        raise ValueError("priority_layers must include at least one layer")

    return MissionPacket(
        incident_name=incident_name.strip(),
        hazard_type=hazard_type.strip(),
        location=location.strip(),
        date_range=date_range.strip(),
        priority_layers=normalized_layers,
        requester=requester.strip(),
        notes=notes.strip(),
    )


def build_codex_prompt(packet: MissionPacket) -> str:
    """Build a Codex CLI-ready prompt from a mission packet."""

    layer_list = ", ".join(packet.priority_layers)
    notes = packet.notes if packet.notes else "No additional notes provided."

    return (
        "You are supporting first responders with rapid geospatial analysis.\n"
        "Create or update a reproducible hazard mapping pipeline in this repository.\n\n"
        f"Incident: {packet.incident_name}\n"
        f"Hazard type: {packet.hazard_type}\n"
        f"Location: {packet.location}\n"
        f"Date range: {packet.date_range}\n"
        f"Priority layers: {layer_list}\n"
        f"Requester: {packet.requester}\n"
        f"Field notes: {notes}\n\n"
        "Execution requirements:\n"
        "1) Use Sentinel data first, then upgrade to commercial imagery only if API keys exist.\n"
        "2) Export outputs as GeoPackage and Cloud-Optimized GeoTIFF.\n"
        "3) Produce a lightweight web viewer for responders.\n"
        "4) Add or update tests for any new logic.\n"
    )


def save_mission_packet(packet: MissionPacket, output_path: str) -> Path:
    """Save mission packet JSON to disk and return the final path."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(packet), indent=2), encoding="utf-8")
    return path


def main() -> None:
    """Command-line helper for generating mission packets and Codex prompts."""

    import argparse

    parser = argparse.ArgumentParser(description="Generate first-responder mission scaffolding")
    parser.add_argument("--incident-name", required=True, help="Incident name")
    parser.add_argument("--hazard-type", required=True, help="Hazard type")
    parser.add_argument("--location", required=True, help="Location description")
    parser.add_argument("--date-range", required=True, help="Date or date range")
    parser.add_argument("--priority-layer", action="append", required=True, help="Layer priority")
    parser.add_argument("--requester", required=True, help="Requesting team")
    parser.add_argument("--notes", default="", help="Optional notes")
    parser.add_argument("--packet-out", default="output/mission_packet.json", help="JSON output path")

    args = parser.parse_args()
    packet = create_mission_packet(
        incident_name=args.incident_name,
        hazard_type=args.hazard_type,
        location=args.location,
        date_range=args.date_range,
        priority_layers=args.priority_layer,
        requester=args.requester,
        notes=args.notes,
    )

    saved_path = save_mission_packet(packet, args.packet_out)
    print(f"Saved mission packet: {saved_path}")
    print("\nCodex prompt:\n")
    print(build_codex_prompt(packet))


if __name__ == "__main__":
    main()
