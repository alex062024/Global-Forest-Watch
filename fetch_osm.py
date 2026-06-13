import requests
import json

overpass_url = "https://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
relation(401017);
out geom;
"""
response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

with open('rfo_osm.json', 'w') as f:
    json.dump(data, f)

print("Données OSM téléchargées.")
