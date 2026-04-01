import streamlit as st
import pandas as pd
import os

# Define the path to the data directory (relative to this file)
DATA_PATH = os.path.join(os.path.dirname(__file__), "data")

@st.cache_data
def load_data(filename):
    file_path = os.path.join(DATA_PATH, filename)
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return None

def get_combined_race_data():
    races = load_data('races.csv')
    results = load_data('results.csv')
    drivers = load_data('drivers.csv')

    if races is None or results is None or drivers is None:
        return None

    merged = pd.merge(results, races, on='raceId', suffixes=('_result', '_race'))
    merged = pd.merge(merged, drivers, on='driverId', suffixes=('', '_driver'))

    return merged

def get_seasons_overview():
    seasons = load_data('seasons.csv')
    races = load_data('races.csv')
    drivers = load_data('drivers.csv')
    circuits = load_data('circuits.csv')

    if any(df is None for df in [seasons, races, drivers, circuits]):
        return None

    races_per_year = races.groupby('year').size().reset_index(name='race_count')
    return {
        'total_seasons': len(seasons),
        'total_races': len(races),
        'total_drivers': len(drivers),
        'total_circuits': len(circuits),
        'races_per_year': races_per_year,
        'year_range': (int(races['year'].min()), int(races['year'].max())),
    }
