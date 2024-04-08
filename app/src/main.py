"""Steamlit app for Alivio project."""

import streamlit as st
import requests
import h3
import pandas as pd
import pydeck as pdk
import re

from project_description import home_page
from viz_hurricane_data import select_and_display_hurricane

def main():
    # Create tabs
    tabs: list[str] = ["Alivio", "Upload Disaster Image", "Hurricane Damage (Historical Data)"]
    selected_tab = st.sidebar.selectbox("Select a tab", tabs)

    if selected_tab == "Alivio":
        home_page()
    # elif selected_tab == "Upload Disaster Image":
    #     st.title("Hurricane Disaster Assessment")
    #     upload_files()
    elif selected_tab == "Hurricane Damage (Historical Data)":
        select_and_display_hurricane()


if __name__ == "__main__":
    main()
