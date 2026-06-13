import osm2geojson
import json

with open('rfo_osm.xml', 'r', encoding='utf-8') as f:
    xml_data = f.read()

geojson_data = osm2geojson.xml2geojson(xml_data)

with open('rfo_boundary.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f)

print("Conversion terminée : rfo_boundary.geojson")
