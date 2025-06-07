from typing import List
import geopandas as gpd
from .stac_search import search_sentinel_scenes, DEFAULT_STAC_URL


def run_pipeline(aoi_path: str, date: str, stac_url: str = DEFAULT_STAC_URL) -> List:
    """Run a simple search pipeline for Sentinel scenes.

    Parameters
    ----------
    aoi_path : str
        Path to a GeoJSON file defining the area of interest.
    date : str
        Date or date range in ISO format (YYYY-MM-DD or YYYY-MM-DD/YYYY-MM-DD).
    stac_url : str, optional
        STAC API endpoint to query, by default ``DEFAULT_STAC_URL``.

    Returns
    -------
    List
        List of STAC items matching the query.
    """
    gdf = gpd.read_file(aoi_path)
    if gdf.empty:
        raise ValueError("AOI file contains no features")
    aoi_geom = gdf.geometry.iloc[0].__geo_interface__
    return search_sentinel_scenes(aoi_geom, date, stac_url=stac_url)


def main() -> None:
    """Command-line entry point for the pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description="Search Sentinel scenes")
    parser.add_argument("aoi", help="Path to AOI GeoJSON")
    parser.add_argument("date", help="Date or date range")
    parser.add_argument(
        "--stac-url",
        default=DEFAULT_STAC_URL,
        help="STAC API endpoint",
    )

    args = parser.parse_args()
    items = run_pipeline(args.aoi, args.date, stac_url=args.stac_url)
    print(f"Found {len(items)} items")


if __name__ == "__main__":
    main()
