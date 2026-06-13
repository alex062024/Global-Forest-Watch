import json
import pandas as pd

# 1. Préparation des données pour le Dashboard
perte_foret = pd.read_csv('perte_foret_rfo_2010_2020.csv')
occupation_sol = pd.read_csv('occupation_sol_rfo_2015.csv')

# 2. Création de la structure HTML du Dashboard
dashboard_html = f'''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard RFO - Global Forest Watch</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ background-color: #f4f7f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        .navbar {{ background-color: #1B4D3E !important; }}
        .card {{ border: none; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }}
        .card-header {{ background-color: #fff; border-bottom: 1px solid #eee; font-weight: bold; color: #1B4D3E; border-radius: 15px 15px 0 0 !important; }}
        .stat-card {{ text-align: center; padding: 20px; color: white; border-radius: 15px; }}
        .bg-forest {{ background-color: #2E8B57; }}
        .bg-loss {{ background-color: #CD5C5C; }}
        .bg-area {{ background-color: #4682B4; }}
        iframe {{ border-radius: 15px; width: 100%; height: 600px; border: none; }}
    </style>
</head>
<body>

<nav class="navbar navbar-dark shadow-sm mb-4">
    <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">🌳 Dashboard de Suivi : Réserve de Faune à Okapis (UNESCO N° 718)</span>
    </div>
</nav>

<div class="container-fluid px-4">
    <!-- Row 1: Key Stats -->
    <div class="row">
        <div class="col-md-4">
            <div class="stat-card bg-area shadow-sm">
                <h5>Surface Totale</h5>
                <h2>1 372 625 Ha</h2>
                <small>Surface protégée (Ituri Forest)</small>
            </div>
        </div>
        <div class="col-md-4">
            <div class="stat-card bg-forest shadow-sm">
                <h5>Couvert Forestier (2015)</h5>
                <h2>93.3%</h2>
                <small>Forêt dense & marécageuse</small>
            </div>
        </div>
        <div class="col-md-4">
            <div class="stat-card bg-loss shadow-sm">
                <h5>Perte Totale (2010-2020)</h5>
                <h2>4 864 Ha</h2>
                <small>Perte de forêt primaire</small>
            </div>
        </div>
    </div>

    <!-- Row 2: Map and Charts -->
    <div class="row mt-4">
        <!-- Map Column -->
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-header">📍 Carte Interactive de l'Occupation du Sol</div>
                <div class="card-body p-0">
                    <iframe src="map_embed.html"></iframe>
                </div>
            </div>
        </div>
        
        <!-- Stats Column -->
        <div class="col-lg-4">
            <div class="card shadow-sm mb-4">
                <div class="card-header">📉 Évolution de la Perte Forestière (Ha)</div>
                <div class="card-body">
                    <canvas id="lossChart"></canvas>
                </div>
            </div>
            <div class="card shadow-sm">
                <div class="card-header">🍰 Occupation du Sol (2015)</div>
                <div class="card-body">
                    <canvas id="landCoverChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <footer class="text-center mt-4 mb-4 text-muted">
        <small>Données : Global Forest Watch, ESA Sentinel-2, UNESCO | Analyse par Gemini CLI</small>
    </footer>
</div>

<script>
    // Chart 1: Loss Evolution
    const ctxLoss = document.getElementById('lossChart').getContext('2d');
    new Chart(ctxLoss, {{
        type: 'line',
        data: {{
            labels: {perte_foret['Annee'].tolist()},
            datasets: [{{
                label: 'Perte de Forêt (Ha)',
                data: {perte_foret['Perte_Foret_Primaire_Ha'].tolist()},
                borderColor: '#CD5C5C',
                backgroundColor: 'rgba(205, 92, 92, 0.1)',
                fill: true,
                tension: 0.3,
                pointRadius: 5
            }}]
        }},
        options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
    }});

    // Chart 2: Land Cover Pie
    const ctxLand = document.getElementById('landCoverChart').getContext('2d');
    new Chart(ctxLand, {{
        type: 'doughnut',
        data: {{
            labels: {occupation_sol['Classe'].tolist()},
            datasets: [{{
                data: {occupation_sol['Pourcentage'].tolist()},
                backgroundColor: ['#006400', '#2E8B57', '#90EE90', '#DAA520', '#1E90FF', '#808080']
            }}]
        }},
        options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
    }});
</script>

</body>
</html>
'''

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_html)

print("Dashboard généré : dashboard.html")
