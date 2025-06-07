import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import hazardwatch.stac_search as stac_search

class FakeSearch:
    def get_items(self):
        return ["item1", "item2"]

class FakeClient:
    last_client = None

    def __init__(self, url):
        self.url = url
        self.last_search = None

    @classmethod
    def open(cls, url):
        client = cls(url)
        cls.last_client = client
        return client

    def search(self, collections, intersects, datetime):
        self.last_search = {
            "collections": collections,
            "intersects": intersects,
            "datetime": datetime,
        }
        return FakeSearch()

def test_search_sentinel_scenes_basic(monkeypatch):
    monkeypatch.setattr(stac_search, "Client", FakeClient)
    # Dummy AOI and date
    aoi = {"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}
    date = "2021-01-01"
    items = stac_search.search_sentinel_scenes(aoi, date, stac_url="https://example.com/api")

    assert items == ["item1", "item2"]
    assert FakeClient.last_client.url == "https://example.com/api"
    expected_datetime = "2021-01-01/2021-01-01"
    assert FakeClient.last_client.last_search == {
        "collections": stac_search.SENTINEL_COLLECTIONS,
        "intersects": aoi,
        "datetime": expected_datetime,
    }

def test_search_sentinel_scenes_with_range(monkeypatch):
    monkeypatch.setattr(stac_search, "Client", FakeClient)
    aoi = {"type": "Point", "coordinates": [0, 0]}
    date_range = "2021-01-01/2021-01-05"
    items = stac_search.search_sentinel_scenes(aoi, date_range)

    assert items == ["item1", "item2"]
    assert FakeClient.last_client.last_search["datetime"] == date_range
