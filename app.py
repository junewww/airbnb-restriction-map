#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

heat_data = pd.read_csv("heat_data.csv")

m = folium.Map(location=[40.7128, -74.0060], zoom_start=11, tiles='cartodbpositron')

heat_layer = folium.FeatureGroup(name='Heatmap', show=True)
heat_points = heat_data.apply(lambda row: [row['lat'], row['long'], row['restriction_score']], axis=1).tolist()
HeatMap(heat_points, radius=8, blur=10, max_zoom=1).add_to(heat_layer)
heat_layer.add_to(m)

marker_layer = folium.FeatureGroup(name='Circle Markers', show=True)
for _, row in heat_data.head(2000).iterrows():
    score = row['restriction_score']
    radius = 1 + score * 1.5     
    opacity = 0.1 + min(score / 5, 0.6) 
    tooltip = f"ID:{row['id']}<br>Neighborhood: {row['neighbourhood group']}<br>Score: {round(score, 2)}<br>HostType: {row['host_type']}"
    
    folium.CircleMarker(
        location=(row['lat'], row['long']),
        radius=radius,
        color='orange',
        fill=True,
        fill_opacity=opacity,
        tooltip=tooltip
    ).add_to(marker_layer)
marker_layer.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

st.title("Airbnb House Rule Restrictiveness Map")
st.markdown("This interactive map visualizes restrictiveness scores based on Airbnb listings. You can explore heatmaps and hover on individual listings to view rule data.")
st_data = st_folium(m, width=1000, height=700)

