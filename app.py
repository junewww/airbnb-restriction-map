#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="Restriction Score Map", layout="wide")

def load_data():
    df = pd.read_csv("heat_data.csv")
    df = df[['lat', 'long', 'restriction_score', 'neighbourhood_group', 'host_type', 'id']].dropna()
    df = df[df['restriction_score'] > 0]
    df['neighbourhood_group'] = df['neighbourhood_group'].astype(str)
    df['id'] = df['id'].astype(str)
    return df

df = load_data()

st.title("🏠 Airbnb Restriction Score Heatmap")
show_markers = st.checkbox("Show Circle Marker", value=True)
max_points = st.slider("most point", 100, 3000, 1000, step=100)

m = folium.Map(location=[40.7128, -74.0060], zoom_start=11, tiles='cartodbpositron')

heat_layer = folium.FeatureGroup(name='Heatmap', show=True)
heat_points = df[['lat', 'long', 'restriction_score']].values.tolist()
HeatMap(heat_points, radius=8, blur=10, max_zoom=1).add_to(heat_layer)
heat_layer.add_to(m)

if show_markers:
    marker_layer = folium.FeatureGroup(name='Circle Markers', show=True)
    for _, row in df.head(max_points).iterrows():
        score = row['restriction_score']
        radius = 1 + score * 1.5
        opacity = 0.1 + min(score / 5, 0.6)
        tooltip = f"ID: {row['id']}<br>Neighborhood: {row['neighbourhood_group']}<br>Score: {round(score, 2)}<br>HostType: {row['host_type']}"
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

st_folium(m, width=1200, height=700)
