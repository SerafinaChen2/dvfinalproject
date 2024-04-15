import streamlit as st
import pandas as pd
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
spotify = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')
spotify['release_date'] = pd.to_datetime(spotify['released_year'].astype(str) + '-' + spotify['released_month'].astype(str).str.zfill(2))

# Sidebar for filtering options
st.sidebar.title("Filter Options")
start_date = st.sidebar.date_input("Start Date", spotify['release_date'].min())
end_date = st.sidebar.date_input("End Date", spotify['release_date'].max())

# Convert dates and filter data
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
filtered_data = spotify[(spotify['release_date'] >= start_date) & (spotify['release_date'] <= end_date)]

# Function to create a bar plot
def create_top_songs_bar_plot(data, top_n):
    data['streams'] = pd.to_numeric(data['streams'], errors='coerce')
    top_songs = data.nlargest(top_n, 'streams')
    fig, ax = plt.subplots()
    ax.bar(top_songs['track_name'], top_songs['streams'])
    ax.set_xticklabels(top_songs['track_name'], rotation=90)
    ax.set_ylabel("Streams")
    ax.set_title("Top Songs Based on Number of Streams")
    return fig

# Radar chart function
def create_radar_chart(data, attributes):
    labels = attributes
    num_vars = len(labels)

    angles = np.linspace(0, 2 * pi, num_vars, endpoint=False).tolist()
    data += data[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, data, color='red', alpha=0.25)
    ax.plot(angles, data, color='red')  # Draw the outline
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    return fig

# User selections from sidebar
top_n_options = [10, 20, 50, 100]
selected_top_n = st.sidebar.selectbox("Select number of top songs to display:", top_n_options)
top_songs_data = create_top_songs_bar_plot(filtered_data, selected_top_n)
st.pyplot(top_songs_data)

# Calculate mean audio features and create radar chart
mean_audio_features = top_songs_data[['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']].mean().tolist()
fig_radar = create_radar_chart(mean_audio_features, ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%'])
st.pyplot(fig_radar)
