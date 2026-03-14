# InstaHazard Map with OpenAI Codex CLI 
One‑hour, chat‑driven remote sensing hazard mapping with OpenAI Codex CLI
⸻

Overview

InstaHazard Map Codex CLI turns a single natural‑language command into a complete, reproducible geospatial workflow that delivers a first post‑disaster damage map in under 60 minutes. It is built on OpenAI Codex CLI, which writes, tests, and runs all code inside a sandboxed Git repository.

Key goals:
	•	Speed – eliminate the ~100 person‑hours now required for statewide change‑detection products.
	•	Flexibility – start with free Sentinel‑1/2 data; auto‑upgrade to PlanetScope or Maxar when API keys exist.
	•	Reproducibility – every step lands in Git, with unit tests and CI.
	•	Openness – MIT licence so agencies can fork and deploy.

Core Features

Stage	What HazardWatch Codex does	Tools
1 📡  Scene search	Builds STAC queries for Sentinel, Planet, Maxar	pystac-client, planet-sdk
2 🌀 Pre‑processing	Reproject, cloud‑mask, radiometric calibration	rioxarray, sentinel‑sat, rasterio
3 🔍 Change detection	Optical diff + SAR backscatter threshold	torchgeo, numpy
4 📦 Packaging	Write GeoPackage & Cloud‑Optimized GeoTIFF	geopandas, gdal
5 🌐 Web viewer	Auto‑generate Folium/Leaflet map	folium

60‑Minute Workflow

# Example: Hurricane Idalia strike, Big Bend FL
codex "Map flood damage for Suwannee County after Idalia, upgrade imagery if Planet key exists"

Codex CLI will:
	1.	Evaluate keys & pick sources (Sentinel‑1/2 → PlanetScope if available).
	2.	Write pipeline.py, run unit tests, fix failing steps.
	3.	Save results to output/ and open viewer.html.

Total runtime on a standard laptop ≈ 55 min for a 5 000 km² AOI.

Quick‑start

# 1  Clone the repo
git clone https://github.com/sounny/hazardwatch-codex.git
cd hazardwatch-codex

# 2  Install dependencies
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3  Install Codex CLI (needs Node 22+)
npm install -g @openai/codex

# 4  Set your OpenAI key & optional imagery keys
export OPENAI_API_KEY=sk-...
export PLANET_API_KEY=...   # optional

# 5  Run the first demo
codex "Map flood damage for Cedar Key after Idalia"


Mission scaffolding CLI
-----------------------
Generate a structured first-responder mission packet and a Codex-ready prompt:

```bash
python -m hazardwatch.mission_scaffold \
  --incident-name "Hurricane Idalia" \
  --hazard-type "Flood" \
  --location "Suwannee County, FL" \
  --date-range "2024-08-30/2024-09-02" \
  --priority-layer "Flood extent" \
  --priority-layer "Road blockage" \
  --requester "Suwannee County EOC" \
  --notes "Prioritize hospitals and shelters"
```

This writes `output/mission_packet.json` and prints a reusable prompt that can be passed to Codex CLI for automated workflow generation.

Browser-based STAC search
-------------------------
If you prefer not to install Python, open ``web/index.html`` in any modern
browser.  Enter a bounding box and date range to query the Planetary Computer
STAC API for recent Sentinel imagery.

Contributing

We welcome PRs! 

License

MIT © 2025 InstaHazard Map Codex contributors

⸻

Built with ❤️ and Codex CLI.
