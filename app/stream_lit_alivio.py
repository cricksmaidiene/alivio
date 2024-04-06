import streamlit as st
import requests
import folium
import h3
from streamlit_folium import folium_static
import geopandas as gpd
import geodatasets
import folium

st.title("Welcome to Alivio! Building Damage Assessment")


def upload_files():
    st.write("### Upload Disaster Image")
    polygon = st.file_uploader("Map polygons", type=["json", "csv"])
    post_image = st.file_uploader("Upload post-disaster image", type=["jpg", "png"])

    if st.button("Assess Damage"):
        if polygon is not None and post_image is not None:
            files = {"polygon": polygon, "post_image": post_image}
            response = requests.post("http://localhost:8000/assess_damage", files=files)
            result = response.json()
            st.write("Assessment Result:", result["result"])
        else:
            st.write("Please upload both map polygon and post image.")

def select_hurricane():
    hurricane = st.selectbox("Select a hurricane", ["Michael", "Harvey", "Florence"])
    display_map(hurricane)

def display_map(map_area):
    st.write("### Map of Disaster Area")
    if map_area == "Michael":
        default_location= (30.1766, -85.8055)  # Florida
        zoom_level = 10
    elif map_area == "Harvey":
        default_location = (27.9947, -97.0469)  # Texas
        zoom_level = 10
    elif map_area == "Florence":
        default_location = (34.2164, -77.8059)  # North Carolina
        zoom_level = 10

    # Create a folium map
    m = folium.Map(location=default_location, zoom_start=zoom_level)

    # Add H3 hexagons to the map
    add_h3_hexagons(m,default_location[0],default_location[1])

    # Render the map using Streamlit
    folium_static(m)
    

def add_h3_hexagons(m,lat,long): 
    # Generate some random hexagon indices for demonstration
    hexagons = h3.k_ring(h3.geo_to_h3(lat,long, 9), 5)  # city hexagons

    # Plot hexagons on the map
    for hexagon in hexagons:
        vertices = h3.h3_to_geo_boundary(hexagon)
        folium.Polygon(locations=vertices, color='blue', fill=True, fill_color='blue', fill_opacity=0.6).add_to(m)


def main():
    st.title('Hurricane Disaster Assessment')

    # Create tabs
    tabs = ["Upload Disaster Image", "Hurricane Damage (Historical Data)"]
    selected_tab = st.sidebar.radio("Select Tab", tabs)

    if selected_tab == "Upload Disaster Image":
        upload_files()
    elif selected_tab == "Hurricane Damage (Historical Data)":
        select_hurricane()
        
    

if __name__ == "__main__":
    main()