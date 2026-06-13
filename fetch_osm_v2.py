import requests
import json

# Essayer différents serveurs Overpass si le premier échoue
servers = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://z.overpass-api.de/api/interpreter"
]

overpass_query = """
[out:json];
relation["name:fr"="Réserve de faune à okapis"];
out geom;
"""

success = False
for server in servers:
    try:
        print(f"Tentative avec {server}...")
        response = requests.get(server, params={'data': overpass_query}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('elements'):
                with open('rfo_boundary.json', 'w') as f:
                    json.dump(data, f)
                print(f"Succès avec {server}")
                success = True
                break
            else:
                print(f"Pas d'éléments trouvés sur {server}")
        else:
            print(f"Erreur {response.status_code} sur {server}")
    except Exception as e:
        print(f"Erreur sur {server}: {e}")

if not success:
    print("Échec de la récupération des données OSM.")
