import json

def map_geojson_point(geojson: str) -> dict:
    return {
        "lat": geojson["coordinates"][1],
        "lon": geojson["coordinates"][0],
    }
