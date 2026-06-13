import json
import pandas as pd

# 1. Charger les données
perte_foret = pd.read_csv('perte_foret_rfo_2010_2020.csv')
occupation_sol = pd.read_csv('occupation_sol_rfo_2015.csv')
with open('rfo_boundary.geojson', 'r') as f:
    rfo_geojson = json.load(f)

# 2. Template HTML Standalone
standalone_html = f'''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard RFO - Standalone Edition</title>
    
    <!-- Bibliothèques externes -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        body {{ background-color: #f0f2f0; font-family: 'Inter', system-ui, -apple-system, sans-serif; }}
        .header-section {{ background: linear-gradient(135deg, #1B4D3E 0%, #2E8B57 100%); color: white; padding: 30px 0; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .card {{ border: none; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); height: 100%; }}
        .card-header {{ background-color: white; border-bottom: 1px solid #eee; font-weight: 700; color: #1B4D3E; padding: 15px 20px; border-radius: 12px 12px 0 0 !important; }}
        .stat-value {{ font-size: 2rem; font-weight: 800; margin: 10px 0; }}
        #map {{ height: 600px; width: 100%; border-radius: 0 0 12px 12px; }}
        .legend-box {{ background: white; padding: 10px; border-radius: 8px; font-size: 12px; line-height: 18px; color: #555; }}
        .legend-key {{ display: inline-block; width: 12px; height: 12px; margin-right: 5px; border-radius: 2px; }}
    </style>
</head>
<body>

<div class="header-section">
    <div class="container text-center">
        <h1 class="display-6 fw-bold">Réserve de Faune à Okapis (RFO)</h1>
        <p class="lead mb-0">Tableau de Bord de Conservation - Patrimoine Mondial UNESCO N° 718</p>
    </div>
</div>

<div class="container mb-5">
    <!-- Row 1: KPI Cards -->
    <div class="row g-4 mb-4">
        <div class="col-md-4">
            <div class="card text-center p-3 border-start border-4 border-primary">
                <div class="text-muted text-uppercase small fw-bold">Surface de la Réserve</div>
                <div class="stat-value text-primary">1 372 625 <span class="fs-5">Ha</span></div>
                <div class="small text-muted">Bassin du Congo, RDC</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-center p-3 border-start border-4 border-success">
                <div class="text-muted text-uppercase small fw-bold">Forêt Intacte (2015)</div>
                <div class="stat-value text-success">93.3 <span class="fs-5">%</span></div>
                <div class="small text-muted">Forêts denses & marécageuses</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-center p-3 border-start border-4 border-danger">
                <div class="text-muted text-uppercase small fw-bold">Perte cumulée (2010-2020)</div>
                <div class="stat-value text-danger">4 864 <span class="fs-5">Ha</span></div>
                <div class="small text-muted">Accélération depuis 2014</div>
            </div>
        </div>
    </div>

    <!-- Row 2: Map and Statistics -->
    <div class="row g-4">
        <!-- Map -->
        <div class="col-lg-8">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <span>📍 Cartographie de l'Occupation du Sol</span>
                    <span class="badge bg-success">Source: UNESCO/OSM</span>
                </div>
                <div id="map"></div>
            </div>
        </div>

        <!-- Charts -->
        <div class="col-lg-4">
            <div class="row g-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">📉 Tendance de Déforestation</div>
                        <div class="card-body">
                            <canvas id="chartPerte"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">🍰 Classes d'Occupation du Sol</div>
                        <div class="card-body">
                            <canvas id="chartSol"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="mt-5 p-4 bg-white rounded-3 shadow-sm border">
        <h5 class="fw-bold border-bottom pb-2">À propos de cette analyse</h5>
        <p class="text-muted small">Ce tableau de bord standalone a été généré pour fournir une vue d'ensemble rapide et précise de l'état de conservation de la RFO. Les données de perte forestière proviennent de l'Université du Maryland (Global Forest Watch) et l'occupation du sol est basée sur les produits ESA Climate Change Initiative.</p>
        <div class="d-flex gap-3">
            <a href="https://whc.unesco.org/fr/list/718/" target="_blank" class="btn btn-outline-dark btn-sm">Fiche UNESCO</a>
            <a href="https://www.globalforestwatch.org/" target="_blank" class="btn btn-outline-success btn-sm">Global Forest Watch</a>
        </div>
    </div>
</div>

<script>
    // --- INITIALISATION DE LA CARTE ---
    const map = L.map('map').setView([2.0, 28.5], 8);

    const esriWorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
        attribution: 'Tiles &copy; Esri'
    }}).addTo(map);

    const rfoBoundary = {json.dumps(rfo_geojson)};
    
    L.geoJSON(rfoBoundary, {{
        style: {{
            color: "#FF4500",
            weight: 3,
            fillColor: "#FF4500",
            fillOpacity: 0.1
        }}
    }}).bindPopup("<b>Réserve de Faune à Okapis</b><br>Limites Officielles").addTo(map);

    // --- GRAPHIQUE PERTE FORESTIÈRE ---
    const ctxPerte = document.getElementById('chartPerte');
    new Chart(ctxPerte, {{
        type: 'line',
        data: {{
            labels: {perte_foret['Annee'].tolist()},
            datasets: [{{
                label: 'Ha perdues',
                data: {perte_foret['Perte_Foret_Primaire_Ha'].tolist()},
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                fill: true,
                tension: 0.3
            }}]
        }},
        options: {{
            plugins: {{ legend: {{ display: false }} }},
            scales: {{ y: {{ beginAtZero: true }} }}
        }}
    }});

    // --- GRAPHIQUE OCCUPATION SOL ---
    const ctxSol = document.getElementById('chartSol');
    new Chart(ctxSol, {{
        type: 'doughnut',
        data: {{
            labels: {occupation_sol['Classe'].tolist()},
            datasets: [{{
                data: {occupation_sol['Pourcentage'].tolist()},
                backgroundColor: ['#1B4D3E', '#2E8B57', '#90EE90', '#DAA520', '#1E90FF', '#808080']
            }}]
        }},
        options: {{
            plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12 }} }} }}
        }}
    }});
</script>

</body>
</html>
'''

with open('standalone_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(standalone_html)

print("Dashboard standalone généré : standalone_dashboard.html")
