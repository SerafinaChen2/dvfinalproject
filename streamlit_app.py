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

# Sidebar for filtering options
st.sidebar.title("Filter Options")

# Create dropdown widgets for start_date and end_date
start_date = st.sidebar.date_input("Start Date", spotify['release_date'].min())
end_date = st.sidebar.date_input("End Date", spotify['release_date'].max())

# Convert start_date and end_date to datetime for filtering
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Create a column 'year_month' to facilitate filtering
spotify['year_month'] = spotify['release_date'].dt.strftime('%Y-%m')

# Filter the data based on the selected date range
filtered_data = spotify[(spotify['release_date'] >= start_date) & (spotify['release_date'] <= end_date)]

# Display the filtered data
st.write("### Displaying data for the selected date range:")
st.write(filtered_data)

