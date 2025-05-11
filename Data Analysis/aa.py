import json

# Load the GeoJSON file
with open("gadm41_NGA_1.json", "r") as f:
    geojson_data = json.load(f)

# Inspect the first feature to check the state format
if "features" in geojson_data and len(geojson_data["features"]) > 0:
    first_feature = geojson_data["features"][0]
    print("First Feature Properties:", first_feature["properties"])
else:
    print("No features found in the GeoJSON file.")