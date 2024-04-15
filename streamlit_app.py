import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import pi

# Set page configuration
st.set_page_config(
    page_title="Spotify Mania",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Spotify data
@st.cache
def load_data():
    data = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')
    data['release_date'] = pd.to_datetime(data['released_year'].astype(str) + '-' + data['released_month'].astype(str).str.zfill(2), errors='coerce')
    return data.dropna(subset=['release_date'])  # Drop rows where 'release_date' is NaT

spotify = load_data()

# Sidebar for filtering options
st.sidebar.title("Filter Options")
if not spotify.empty:
    min_date, max_date = spotify['release_date'].min(), spotify['release_date'].max()
    start_date = st.sidebar.date_input("Start Date", min_date)
    end_date = st.sidebar.date_input("End Date", max_date)

    # Convert dates and filter data
    filtered_data = spotify[(spotify['release_date'] >= start_date) & (spotify['release_date'] <= end_date)]

    # Define functions for plots
    def create_top_songs_bar_plot(data, top_n):
        data['streams'] = pd.to_numeric(data['streams'], errors='coerce')
        top_songs = data.nlargest(top_n, 'streams')
        fig, ax = plt.subplots()
        ax.bar(top_songs['track_name'], top_songs['streams'])
        ax.set_xticklabels(top_songs['track_name'], rotation=90)
        ax.set_ylabel("Streams")
        ax.set_title("Top Songs Based on Number of Streams")
        return top_songs, fig

    def create_radar_chart(data, attributes):
        labels = attributes
        num_vars = len(labels)
        angles = np.linspace(0, 2 * pi, num_vars, endpoint=False).tolist()
        data += data[:1]
        angles += angles[:1]
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, data, color='red', alpha=0.25)
        ax.plot(angles, data, color='red')
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        return fig

    # User selections from sidebar
    top_n_options = [10, 20, 50, 100]
    selected_top_n = st.sidebar.selectbox("Select number of top songs to display:", top_n_options)
    top_songs_data, top_songs_plot = create_top_songs_bar_plot(filtered_data, selected_top_n)
    st.pyplot(top_songs_plot)

    # Calculate mean audio features and create radar chart
    if not top_songs_data.empty:
        mean_audio_features = top_songs_data[['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']].mean().tolist()
        fig_radar = create_radar_chart(mean_audio_features, ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%'])
        st.pyplot(fig_radar)
    else:
        st.warning("No data available for selected top songs.")
else:
    st.error("No data loaded. Please check the data source or path.")
