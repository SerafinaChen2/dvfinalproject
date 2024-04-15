import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Spotify Mania",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.header("Most Streamed Spotify Songs 2023", divider="rainbow")

col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown("Team Members: Luanqi CHEN, Mingjing HE, Josué LABRIN, Vennela SEELAM") 
with col2:
    st.image('https://blog.cloudflare.com/content/images/2017/10/Spotify_Logo_RGB_Green-1.png', 
         width=180)
    
st.subheader("Overview of the project")
st.markdown("This project conducts an analysis of the top songs of 2023 on Spotify,"
            " using a dataset that includes track names, artist information, release dates, Spotify playlist and chart appearances, streaming statistics, and presence on other platforms like Apple Music, Deezer, and Shazam."
            " It explores the success factors of songs and artists in the modern, "
            " streaming-dominated music industry, providing insights that are crucial for artists and producers.")

# Load Spotify data
spotify = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')
spotify['release_date'] = pd.to_datetime(spotify['released_year'].astype(str) + '-' + spotify['released_month'].astype(str).str.zfill(2))

# ------ Visualisation 1 ---------
st.subheader("Top tracks plot and Radar plot with Attributes")

# Sidebar for filtering options
st.sidebar.title("Filter Options")

# Create dropdown widgets for start_date and end_date
start_date = st.sidebar.date_input("Start Date", spotify['release_date'].min(), min_value=spotify['release_date'].min(), max_value=spotify['release_date'].max())
end_date = st.sidebar.date_input("End Date", spotify['release_date'].max(), min_value=spotify['release_date'].min(), max_value=spotify['release_date'].max())

# Convert start_date and end_date to datetime for filtering
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Function to filter and retrieve top songs
def get_top_songs(data, top_n):
    data['streams'] = pd.to_numeric(data['streams'], errors='coerce')
    return data[(data['release_date'] >= start_date) & (data['release_date'] <= end_date)].nlargest(top_n, 'streams')

# Sidebar options for selecting number of top songs
top_n_options = [10, 20, 50, 100]
selected_top_n = st.selectbox("Select number of top songs to display:", top_n_options)

# Retrieve the top songs based on user selection
top_songs_data = get_top_songs(spotify, selected_top_n)

# Function to create and display top songs bar plot
def display_top_songs_bar_plot(top_songs):
    fig_bar = px.bar(top_songs, x='track_name', y='streams', title='Top Songs Based on Number of Streams')
    return fig_bar

# Calculate mean audio features for selected top tracks
mean_audio_features = top_songs_data[['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']].mean().tolist()
attributes = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']
mean_audio_df = pd.DataFrame({'attribute': attributes, 'mean_value': mean_audio_features})
fig_radar = px.line_polar(mean_audio_df, r='mean_value', theta='attribute', line_close=True, title='Radar Plot of Mean Audio Features')
fig_radar.update_traces(fill='toself')

# Display the bar plot and radar chart side by side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(display_top_songs_bar_plot(top_songs_data))
with col2:
    st.plotly_chart(fig_radar)

# ------ Visualisation 2 ---------
st.subheader("Top Artist Plot by number of streams")

# Create a column 'year_month' to facilitate filtering
spotify['year_month'] = spotify['release_date'].dt.strftime('%Y-%m')

# Filter the data based on the selected date range
filtered_data = spotify[(spotify['release_date'] >= start_date) & (spotify['release_date'] <= end_date)]

# Function to create top artists bar plot
def create_top_artists_bar_plot(data, top_n):
    # Group the data by artist and sum the streams
    artist_streams = data.groupby('artist(s)_name')['streams'].sum().reset_index()

    # Sort the data by total streams and select top N artists
    top_artists = artist_streams.nlargest(top_n, 'streams')

    # Create the bar plot
    chart = alt.Chart(top_artists).mark_bar().encode(
        x='streams:Q',
        y=alt.Y('artist(s)_name:N', sort='-x'),
        color=alt.Color('streams:Q', scale=alt.Scale(scheme='viridis'), legend=None),
        tooltip=['artist(s)_name', 'streams']
    ).properties(
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )
    return chart

# Sidebar options for selecting number of top artists to display
top_n_options_artists = [3, 5, 10]
selected_top_n_artists = st.selectbox("Select number of top artists to display:", top_n_options_artists)

# Create and display the top artists bar plot
st.altair_chart(create_top_artists_bar_plot(filtered_data, selected_top_n_artists), use_container_width=True)

# ------ Visualisation 3 ---------
st.subheader("Historical Trend of number of tracks")

def create_tracks_evolution_plot(data, time_unit):
    # Convert release_date to string for grouping
    data['release_date_str'] = data['release_date'].dt.strftime('%Y-%m')  # Format as year-month string

    # Group the data by release date string and count the number of tracks
    if time_unit == 'Year':
        tracks_evolution = data.groupby(data['release_date_str'].str[:4])['track_name'].nunique().reset_index()
        x_axis_title = 'Year'
    elif time_unit == 'Month':
        tracks_evolution = data.groupby(data['release_date_str'])['track_name'].nunique().reset_index()
        x_axis_title = 'Month'

    # Create the line plot
    chart = alt.Chart(tracks_evolution).mark_line().encode(
        x=alt.X('release_date_str:O', title=x_axis_title),
        y=alt.Y('track_name:Q', title='Number of Tracks'),
        tooltip=['release_date_str:O', 'track_name:Q']
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )

    return chart

# Sidebar options for selecting time unit (Month or Year)
time_unit_options = ['Month', 'Year']
selected_time_unit = st.selectbox("Select time unit:", time_unit_options)

# Create and display the tracks evolution plot
st.write("### Evolution of Number of Tracks Over Time")
st.altair_chart(create_tracks_evolution_plot(spotify, selected_time_unit), use_container_width=True)

# ------ Visualisation 4 ---------
st.subheader("Average Musical Characteristics of Trending Tracks Over Time")

# Unique month-year values
spotify['month_years'] = spotify['release_date'].dt.strftime('%Y-%m')
month_years = sorted(spotify['month_years'].unique())

# Streamlit selectors for start and end dates
start_date = st.selectbox('Start Date', month_years, index=0)
end_date = st.selectbox('End Date', month_years, index=len(month_years) - 1)

# Filter data based on selection
filtered_data = spotify[(spotify['month_years'] >= start_date) & (spotify['month_years'] <= end_date)]

# Create an interval selection to select points within a rectangular area
selection = alt.selection_interval(encodings=['x', 'y'])

# Scatter plot
scatter_base = alt.Chart(filtered_data).properties(width=800, height=300)
scatter = scatter_base.mark_point().encode(
    x='release_date:T',
    y='streams:Q',
    color=alt.condition(selection, alt.value('blue'), alt.value('lightgray')),
    tooltip=['track_name:N', 'artist(s)_name:N', 'streams:Q', 'release_date:T']
).add_selection(
    selection
)

# Bar plot for musical characteristics
bar_base = alt.Chart(filtered_data).properties(width=800, height=100)
bars = bar_base.mark_bar().encode(
    x=alt.X('Percentage:Q', title='Average Percentage'),
    y=alt.Y('Musical Characteristic:N', title='Musical Characteristics'),
    color=alt.Color('Musical Characteristic:N',
                    scale=alt.Scale(domain=['Danceability', 'Valence', 'Energy'],
                                    range=['#e94f13', '#989681', '#e69138'])),
    tooltip=['Percentage:Q']
).transform_filter(
    selection
).transform_aggregate(
    Danceability='mean(danceability_%)',
    Valence='mean(valence_%)',
    Energy='mean(energy_%)',
    groupby=['track_name']
).transform_fold(
    ['Danceability', 'Valence', 'Energy'],
    as_=['Musical Characteristic', 'Percentage']
)

# Concatenate the scatter and bar plots vertically
chart = alt.vconcat(scatter, bars)

# Display the concatenated chart
st.altair_chart(chart, use_container_width=True)
