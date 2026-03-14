import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json

import pytest

from hazardwatch.mission_scaffold import (
    MissionPacket,
    build_codex_prompt,
    create_mission_packet,
    save_mission_packet,
)


def test_create_mission_packet_normalizes_layers_and_fields():
    packet = create_mission_packet(
        incident_name="  Idalia  ",
        hazard_type=" flood ",
        location=" Suwannee County, FL ",
        date_range=" 2024-08-30/2024-09-02 ",
        priority_layers=[" flood extent ", "", " road blockage "],
        requester=" County EOC ",
        notes="  prioritize hospitals  ",
    )

    assert packet == MissionPacket(
        incident_name="Idalia",
        hazard_type="flood",
        location="Suwannee County, FL",
        date_range="2024-08-30/2024-09-02",
        priority_layers=["flood extent", "road blockage"],
        requester="County EOC",
        notes="prioritize hospitals",
    )


def test_create_mission_packet_requires_layer():
    with pytest.raises(ValueError, match="priority_layers"):
        create_mission_packet(
            incident_name="Incident",
            hazard_type="wildfire",
            location="Somewhere",
            date_range="2024-01-01",
            priority_layers=["   ", ""],
            requester="Requester",
        )


def test_build_codex_prompt_includes_key_sections():
    packet = MissionPacket(
        incident_name="Idalia",
        hazard_type="flood",
        location="Suwannee County, FL",
        date_range="2024-08-30/2024-09-02",
        priority_layers=["flood extent", "damaged structures"],
        requester="County EOC",
        notes="",
    )

    prompt = build_codex_prompt(packet)

    assert "Incident: Idalia" in prompt
    assert "Priority layers: flood extent, damaged structures" in prompt
    assert "No additional notes provided." in prompt
    assert "Use Sentinel data first" in prompt


def test_save_mission_packet(tmp_path):
    packet = MissionPacket(
        incident_name="Idalia",
        hazard_type="flood",
        location="Suwannee County, FL",
        date_range="2024-08-30/2024-09-02",
        priority_layers=["flood extent"],
        requester="County EOC",
        notes="",
    )

    output = tmp_path / "packet.json"
    saved = save_mission_packet(packet, str(output))

    assert saved == output
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["incident_name"] == "Idalia"
    assert data["priority_layers"] == ["flood extent"]
