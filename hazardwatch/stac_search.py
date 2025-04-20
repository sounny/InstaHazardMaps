from typing import List
from pystac_client import Client

DEFAULT_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
SENTINEL_COLLECTIONS = ["sentinel-1-grd", "sentinel-2-l2a"]

def search_sentinel_scenes(aoi: dict, date: str, stac_url: str = DEFAULT_STAC_URL) -> List:
    """
    Search for Sentinel-1 and Sentinel-2 scene items for the given AOI and date.

    Parameters:
        aoi (dict): GeoJSON-like geometry for spatial search.
        date (str): Date in ISO format (YYYY-MM-DD) or datetime range (YYYY-MM-DD/YYYY-MM-DD).
        stac_url (str): STAC API URL to query.

    Returns:
        List of pystac.Item objects matching Sentinel-1 and Sentinel-2 collections.
    """
    client = Client.open(stac_url)
    # Use date range if a single date is provided
    datetime_range = date if "/" in date else f"{date}/{date}"
    search = client.search(
        collections=SENTINEL_COLLECTIONS,
        intersects=aoi,
        datetime=datetime_range
    )
    items = list(search.get_items())
    return items