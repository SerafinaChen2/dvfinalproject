import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(
    page_title="Spotify Mania",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable dark theme for Altair
alt.themes.enable("dark")

# Load Spotify data
spotify = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')
spotify['release_date'] = pd.to_datetime(spotify['released_year'].astype(str) + '-' + spotify['released_month'].astype(str).str.zfill(2))

# Unique month-year values
month_years = sorted(spotify['month_year'].unique())

# Streamlit selectors for start and end dates
start_date = st.selectbox('Start Date', month_years, index=0)
end_date = st.selectbox('End Date', month_years, index=len(month_years) - 1)

# Filter data based on selection
filtered_data = spotify[(spotify['month_year'] >= start_date) & (spotify['month_year'] <= end_date)]

# Base chart for scatter plot
scatter_base = alt.Chart(filtered_data).properties(width=800, height=300)
scatter = scatter_base.mark_point().encode(
    x='release_date:T',
    y='streams:Q',
    tooltip=['track_name:N', 'artist(s)_name:N', 'streams:Q', 'release_date:T', 'bpm:Q']
)

# Display scatter plot
st.altair_chart(scatter, use_container_width=True)

# Base chart for bar plot
bar_base = alt.Chart(filtered_data).properties(width=800, height=100)
bars = bar_base.mark_bar().encode(
    x=alt.X('Percentage:Q', title='Average Percentage'),
    y=alt.Y('Musical Characteristic:N', title='Musical Characteristics'),
    color=alt.Color('Musical Characteristic:N', scale=alt.Scale(domain=['Danceability', 'Valence', 'Energy'], range=['#e94f13', '#989681', '#e69138'])),
    tooltip=['Percentage:Q']
).transform_aggregate(
    Danceability='mean(danceability_%)',
    Valence='mean(valence_%)',
    Energy='mean(energy_%)',
    groupby=['track_name']
).transform_fold(
    ['Danceability', 'Valence', 'Energy'],
    as_=['Musical Characteristic', 'Percentage']
)

# Display bar plot
st.altair_chart(bars, use_container_width=True)
