import streamlit as st
import requests
import h3
import pandas as pd
import pydeck as pdk
import re

def main_page():
    st.title("Welcome to Alivio!")
    st.title("Building Damage Assessment")
    st.write("#### About our Project:")
    about_us= """
    Disaster relief organizations face significant hurdles in efficiently identifying and assisting populations vulnerable to or affected by natural disasters. The core of the problem lies in the inability to quickly and accurately assess the potential for disaster impact and the extent of damage post-disaster. This challenge is amplified by:

    Infrastructure & Resources: The resilience of buildings and infrastructure to withstand natural disasters is a critical factor. Efficient allocation of resources, both in terms of disaster preparedness and response, is crucial. Misallocation can lead to ineffective disaster management, resulting in increased casualties and property damage.

    Alivio is built by utilizing the foundation computer vision model - Visual Transformer as its backbone and aims to provide a cohesive solution for rescue team member with not only identifying the building damage by severity but also identifies vulnerable populations in the affected area.
    """
    st.markdown(about_us)

def upload_files():
    st.write("### Upload Disaster Image ")
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
    hurricane = st.selectbox("Select a hurricane", ["Michael", "Harvey", "Florence", "Matthew"])
    display_map(hurricane)

def display_map(map_area):
    st.write("### Map of Disaster Area")
    h3_layer = st.selectbox("Select H3 level", ["None","6", "7"])

    map_layers = []
  

    if map_area == "Michael":
        lat= 30.1698
        long = -85.6514  # Florida
        zoom_level = 14
        view_state = pdk.ViewState(latitude=lat , longitude=long, zoom=zoom_level)
        df = pd.read_csv("michael_polygons.csv")
        df = parse_and_create_new_column(df, 'wkt_lt_lg', 'parsed_polygon')
        df['color'] = lambda row: get_color(row['damage_level'])

       
        polygon_layer = pdk.Layer(
            "PolygonLayer",
            df,
            stroked=True,
            get_polygon="parsed_polygon",
            filled=True,
            extruded=False,
            get_fill_color="color",
            get_line_color=[255, 255, 255],
            auto_highlight=True,
            pickable=True,
            )
        tool_tip =  {"text": "Damage: {damage_level}"}
        map_layers.append(polygon_layer)

    elif map_area == "Harvey":
        default_location = (27.9947, -97.0469)  # Texas
        zoom_level = 10
    elif map_area == "Florence":
        default_location = (34.2164, -77.8059)  # North Carolina
        zoom_level = 10

    # add h3 layer
    if h3_layer != "None":
        map_layers.append(render_h3_layer(h3_layer))

    #render map
    r = pdk.Deck(layers=map_layers, initial_view_state=view_state,tooltip=tool_tip)
    st.pydeck_chart(r)

def parse_polygon_coordinates(polygon_str):
    # Extracting coordinates from the string using regular expression
    coordinates = re.findall(r"[-+]?\d*\.\d+|\d+", polygon_str)
    # Converting coordinates to a list of tuples
    coordinates = [[float(coordinates[i]), float(coordinates[i + 1])] for i in range(0, len(coordinates), 2)]
    return coordinates

def parse_and_create_new_column(df, original_column_name, new_column_name):
    # Apply parsing function to the original column
    df[new_column_name] = df[original_column_name].apply(parse_polygon_coordinates)
    return df

def get_color(damage_category):
    if damage_category == "destroyed":
        return [255, 0, 0]  # Red color for severe damage
    elif damage_category == "major-damage":
        return [255, 255, 0]  # Yellow color for major damage
    elif damage_category == "minor-damage":
        return [0, 0, 255]  # Blue color for minor damage
    elif damage_category == "no-damage":
        return [0, 255, 0]  # Gree color for no damage
    else:
        return [128, 128, 128]  # Gray color for unknown category

def render_h3_layer(layer):
    df6 = pd.read_csv('merged_df_h3_cell_6.csv')
    df7 = pd.read_csv('merged_df_h3_cell_7.csv')
    df8 = pd.read_csv('merged_df_h3_cell_8.csv')

    if layer == "6":
        pdk_layer = pdk.Layer(
            "H3HexagonLayer",
            df6,
            pickable=True,
            stroked=True,
            filled=True,
            extruded=False,
            get_hexagon="h3_cell_6",
            get_fill_color="[255-gdp_per_capita, 255, gdp_per_capita]",
            opacity = 0.5,
            get_line_color=[255, 255, 255],
            line_width_min_pixels=2,
            )
    elif layer == "7":
        pdk_layer = pdk.Layer(
            "H3HexagonLayer",
            df7,
            pickable=True,
            stroked=True,
            filled=True,
            extruded=False,
            get_hexagon="h3_cell_6",
            get_fill_color="[0, 255, gdp_per_capita]",
            get_line_color=[255, 255, 255],
            line_width_min_pixels=2,
            )

    return pdk_layer

def main():
    
    # Create tabs
    tabs = ["Alivio", "Upload Disaster Image", "Hurricane Damage (Historical Data)"]
    selected_tab = st.sidebar.radio("Select Tab", tabs)

    if selected_tab == "Alivio":
        main_page()
    elif selected_tab == "Upload Disaster Image":
        st.title('Hurricane Disaster Assessment')
        upload_files()
    elif selected_tab == "Hurricane Damage (Historical Data)":
        st.title('Previous Hurricane Disasters')
        select_hurricane()
        
    

if __name__ == "__main__":
    main()