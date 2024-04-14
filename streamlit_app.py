import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np

pd.set_option('display.max_columns', None)

# Set page configuration
st.set_page_config(
    page_title="Spotify Mania",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Enable dark theme for Altair
alt.themes.enable("dark")
