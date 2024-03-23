import streamlit as st
import requests

st.title("Welcome to Alivio! Building Damage Assessment")


def upload_images():
    st.write("### Upload Pre and Post Images")
    pre_image = st.file_uploader("Upload pre-disaster image", type=["jpg", "png"])
    post_image = st.file_uploader("Upload post-disaster image", type=["jpg", "png"])

    if st.button("Assess Damage"):
        if pre_image is not None and post_image is not None:
            files = {"pre_image": pre_image, "post_image": post_image}
            response = requests.post("http://localhost:8000/assess_damage", files=files)
            result = response.json()
            st.write("Assessment Result:", result["result"])
        else:
            st.write("Please upload both pre and post images.")

def select_hurricane():
    hurricane = st.selectbox("Select a hurricane", ["Michael", "Harvey", "Florence"])

def display_map():
    st.write("### Foursquare Map of Disaster Area")
    # Add your Foursquare map display logic here
    st.write("Map Placeholder")

def main():
    st.title('Hurricane Disaster Assessment')

    # Create tabs
    tabs = ["Upload Images", "Hurricane Damage (Historical Data)"]
    selected_tab = st.sidebar.radio("Select Tab", tabs)

    if selected_tab == "Upload Images":
        upload_images()
    elif selected_tab == "Hurricane Damage (Historical Data)":
        select_hurricane()
        display_map()
    

if __name__ == "__main__":
    main()