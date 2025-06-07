import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import hazardwatch.pipeline as pipeline


class DummyGDF(gpd.GeoDataFrame):
    pass


def fake_read_file(path):
    data = {'geometry': [Point(0, 0)]}
    return gpd.GeoDataFrame(data, geometry='geometry', crs='EPSG:4326')


def test_run_pipeline(monkeypatch):
    monkeypatch.setattr(gpd, 'read_file', fake_read_file)
    # Patch search_sentinel_scenes to avoid network call
    def fake_search(aoi, date, stac_url):
        return ['item']

    monkeypatch.setattr(pipeline, 'search_sentinel_scenes', fake_search)

    items = pipeline.run_pipeline('dummy.geojson', '2024-01-01')
    assert items == ['item']

