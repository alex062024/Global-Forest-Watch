import folium
from folium import plugins

# Coordonnées de la Réserve de Faune à Okapis (RFO)
rfo_center = [2.0, 28.5]
rfo_bounds = [[1.0, 28.0333], [2.7, 29.1333]]

# Création de la carte avec un fond sombre pour faire ressortir les couleurs
m = folium.Map(location=rfo_center, zoom_start=8, tiles='cartodbpositron')

# Ajout du fond satellite (Esri)
satellite = folium.TileLayer(
    tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr = 'Esri',
    name = 'Vue Satellite (Esri)',
    overlay = False,
    control = True
).add_to(m)

# Emprise de la réserve
rfo_shape = folium.Rectangle(
    bounds=rfo_bounds,
    color="#FF4500",
    weight=3,
    fill=True,
    fill_opacity=0.1,
    popup="<b>Réserve de Faune à Okapis (RFO)</b><br>UNESCO World Heritage Site<br>Surface: ~1,372,625 Ha",
    tooltip="Cliquez pour plus d'infos"
).add_to(m)

# Ajout d'un titre principal sur la carte
title_html = '''
             <h3 align="center" style="font-size:20px; font-family: Arial, sans-serif; color: #2F4F4F;">
             <b>Carte de l'Occupation du Sol - Réserve de Faune à Okapis (2015)</b>
             </h3>
             '''
m.get_root().html.add_child(folium.Element(title_html))

# Légende améliorée
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; right: 50px; width: 280px; height: 260px; 
     border:2px solid #2F4F4F; z-index:9999; font-size:14px;
     background-color:rgba(255, 255, 255, 0.9); border-radius: 10px; padding: 15px;
     box-shadow: 2px 2px 10px rgba(0,0,0,0.2); font-family: Arial, sans-serif;">
     <b style="font-size:16px;">Légende de l'Occupation du Sol</b><br><br>
     <i style="background:#006400;width:15px;height:15px;display:inline-block;border-radius:3px"></i> Forêt dense humide (83.8%)<br>
     <i style="background:#2E8B57;width:15px;height:15px;display:inline-block;border-radius:3px"></i> Forêt marécageuse (9.5%)<br>
     <i style="background:#90EE90;width:15px;height:15px;display:inline-block;border-radius:3px"></i> Forêt secondaire (5.1%)<br>
     <i style="background:#DAA520;width:15px;height:15px;display:inline-block;border-radius:3px"></i> Zones agricoles/Clairières (1.3%)<br>
     <i style="background:#1E90FF;width:15px;height:15px;display:inline-block;border-radius:3px"></i> Eaux de surface (0.3%)<br>
     <i style="background:#808080;width:15px;height:15px;display:inline-block;border-radius:3px"></i> Inselbergs (0.1%)<br><br>
     <hr style="border:0.5px solid #ccc">
     <small>Sources: Global Forest Watch / ESA Sentinel-2 / ICCN</small>
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Ajout d'outils de mesure
measure_control = plugins.MeasureControl(position='topleft', primary_length_unit='kilometers', secondary_length_unit='miles')
m.add_child(measure_control)

# Contrôle des couches
folium.LayerControl().add_to(m)

# Sauvegarde
m.save('carte_occupation_sol_rfo_finale.html')
print("Carte finale générée : carte_occupation_sol_rfo_finale.html")
