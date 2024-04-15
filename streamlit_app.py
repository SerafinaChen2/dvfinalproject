pip install plotly
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Spotify Mania",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Spotify data and prepare it
spotify = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')
spotify['release_date'] = pd.to_datetime(spotify['released_year'].astype(str) + '-' + spotify['released_month'].astype(str).str.zfill(2))

# Sidebar for filtering options
st.sidebar.title("Filter Options")
start_date = st.sidebar.date_input("Start Date", spotify['release_date'].min())
end_date = st.sidebar.date_input("End Date", spotify['release_date'].max())

# Filter the data based on the selected date range
filtered_data = spotify[(spotify['release_date'] >= start_date) & (spotify['release_date'] <= end_date)]
st.write("### Displaying data for the selected date range:")
st.write(filtered_data)

# Function to create top songs bar plot
def create_top_songs_bar_plot(data, top_n):
    data['streams'] = pd.to_numeric(data['streams'], errors='coerce')
    return data.nlargest(top_n, 'streams')

# Sidebar option for number of top songs
top_n_options = [10, 20, 50, 100]
selected_top_n = st.sidebar.selectbox("Select number of top songs to display:", top_n_options)

# Display top songs based on streams
top_songs_data = create_top_songs_bar_plot(filtered_data, selected_top_n)
st.write("### Top Songs Based on Number of Streams")
st.write(top_songs_data)

# Radar chart for audio features
mean_audio_features = top_songs_data[['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']].mean().tolist()
attributes = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']
mean_audio_df = pd.DataFrame({'attribute': attributes, 'mean_value': mean_audio_features})

fig = px.line_polar(mean_audio_df, r='mean_value', theta='attribute', line_close=True)
fig.update_traces(fill='toself')
st.write("### Radar Plot of Mean Audio Features")
st.plotly_chart(fig)
