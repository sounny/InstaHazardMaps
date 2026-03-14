import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json

import hazardwatch.cli as cli


class FakeItem:
    def __init__(self, item_id, collection_id, dt):
        self.id = item_id
        self.collection_id = collection_id
        self.properties = {"datetime": dt}


def test_search_human_output(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "run_pipeline",
        lambda aoi, date, stac_url: [
            FakeItem("A", "sentinel-2-l2a", "2025-01-01T00:00:00Z"),
            FakeItem("B", "sentinel-1-grd", "2025-01-02T00:00:00Z"),
        ],
    )

    rc = cli.main(["search", "aoi.geojson", "2025-01-01/2025-01-05", "--limit", "1"])

    output = capsys.readouterr().out
    assert rc == 0
    assert "Found 2 scene(s); showing 1" in output
    assert "1. A [sentinel-2-l2a]" in output


def test_search_json_output(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "run_pipeline",
        lambda aoi, date, stac_url: [
            {"id": "item-1", "collection": "sentinel-1-grd", "properties": {"datetime": "2025-01-01T00:00:00Z"}}
        ],
    )

    rc = cli.main(["search", "aoi.geojson", "2025-01-01", "--json"])

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert rc == 0
    assert payload["count"] == 1
    assert payload["results"][0]["id"] == "item-1"


def test_sources_human_output(capsys):
    rc = cli.main(["sources"])

    output = capsys.readouterr().out
    assert rc == 0
    assert "STAC endpoint:" in output
    assert "- sentinel-1-grd" in output


def test_plan_json_output(capsys):
    rc = cli.main(["plan", "--json"])

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert rc == 0
    assert payload["workflow"] == "scene-discovery"
    assert len(payload["steps"]) >= 3


def test_banner_shows_for_tty_non_json(monkeypatch, capsys):
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True)

    rc = cli.main(["sources"])

    output = capsys.readouterr().out
    assert rc == 0
    assert "InstaHazard Maps CLI" in output


def test_banner_hidden_for_json_output(monkeypatch, capsys):
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True)

    rc = cli.main(["plan", "--json"])

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert rc == 0
    assert payload["workflow"] == "scene-discovery"


def test_banner_can_be_disabled_with_env(monkeypatch, capsys):
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True)
    monkeypatch.setenv("HAZARDWATCH_NO_BANNER", "1")

    rc = cli.main(["sources"])

    output = capsys.readouterr().out
    assert rc == 0
    assert "InstaHazard Maps CLI" not in output
