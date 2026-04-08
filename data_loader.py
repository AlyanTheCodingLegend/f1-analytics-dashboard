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

@st.cache_data
def get_combined_race_data():
    races = load_data('races.csv')
    results = load_data('results.csv')
    drivers = load_data('drivers.csv')

    if races is None or results is None or drivers is None:
        return None

    # Merge Results with Races
    merged = pd.merge(results, races, on='raceId', suffixes=('_result', '_race'))

    # Merge with Drivers
    merged = pd.merge(merged, drivers, on='driverId', suffixes=('', '_driver'))

    # Null handling and type coercion
    merged['points'] = pd.to_numeric(merged['points'], errors='coerce').fillna(0)
    merged['positionOrder'] = pd.to_numeric(merged['positionOrder'], errors='coerce')
    merged['grid'] = pd.to_numeric(merged['grid'], errors='coerce')
    merged.dropna(subset=['positionOrder'], inplace=True)

    return merged

def get_speed_data():
    races = load_data('races.csv')
    results = load_data('results.csv')
    circuits = load_data('circuits.csv')

    if races is None or results is None or circuits is None:
        return None

    race_results = pd.merge(results, races[['raceId', 'year', 'circuitId', 'name']], on='raceId')
    full_data = pd.merge(race_results, circuits[['circuitId', 'name', 'location', 'country']], on='circuitId', suffixes=('_race', '_circuit'))

    full_data['fastestLapSpeed'] = pd.to_numeric(full_data['fastestLapSpeed'], errors='coerce')
    speed_data = full_data.dropna(subset=['fastestLapSpeed'])

    return speed_data

def get_dominance_data():
    races = load_data('races.csv')
    results = load_data('results.csv')
    constructors = load_data('constructors.csv')

    if races is None or results is None or constructors is None:
        return None

    race_results = pd.merge(results, races[['raceId', 'year']], on='raceId')
    full_data = pd.merge(race_results, constructors[['constructorId', 'name']], on='constructorId', suffixes=('_race', '_const'))

    yearly_points = full_data.groupby(['year', 'name'])['points'].sum().reset_index()
    yearly_totals = yearly_points.groupby('year')['points'].sum().reset_index().rename(columns={'points': 'total_year_points'})

    merged_points = pd.merge(yearly_points, yearly_totals, on='year')
    merged_points['points_share'] = (merged_points['points'] / merged_points['total_year_points']) * 100

    return merged_points

def get_quali_vs_race_data():
    """
    Prepares data for 'Qualifying Merchants vs Race Monsters'.
    """
    results = load_data('results.csv')
    drivers = load_data('drivers.csv')

    if results is None or drivers is None:
        return None

    merged = pd.merge(results, drivers[['driverId', 'code', 'surname']], on='driverId')

    counts = merged['driverId'].value_counts()
    experienced_drivers = counts[counts > 50].index

    filtered = merged[merged['driverId'].isin(experienced_drivers)].copy()
    filtered = filtered[filtered['grid'] > 0]

    stats = filtered.groupby(['driverId', 'code', 'surname']).agg({
        'grid': 'mean',
        'positionOrder': 'mean',
        'raceId': 'count'
    }).reset_index()

    stats.columns = ['driverId', 'code', 'surname', 'avg_grid', 'avg_finish', 'races']
    stats['net_gain'] = stats['avg_grid'] - stats['avg_finish']

    return stats

def get_driver_standings_evolution():
    standings = load_data('driver_standings.csv')
    races = load_data('races.csv')
    drivers = load_data('drivers.csv')

    if any(df is None for df in [standings, races, drivers]):
        return None

    merged = pd.merge(standings, races[['raceId', 'year', 'round', 'name']], on='raceId')
    merged = pd.merge(merged, drivers[['driverId', 'surname', 'code', 'nationality']], on='driverId')
    merged['points'] = pd.to_numeric(merged['points'], errors='coerce').fillna(0)
    merged['wins'] = pd.to_numeric(merged['wins'], errors='coerce').fillna(0)
    return merged

def get_constructor_results_data():
    con_results = load_data('constructor_results.csv')
    races = load_data('races.csv')
    constructors = load_data('constructors.csv')

    if any(df is None for df in [con_results, races, constructors]):
        return None

    con_results['points'] = pd.to_numeric(con_results['points'], errors='coerce').fillna(0)
    merged = pd.merge(con_results, races[['raceId', 'year', 'round', 'name']], on='raceId')
    merged = pd.merge(merged, constructors[['constructorId', 'name']], on='constructorId',
                      suffixes=('_race', '_team'))
    return merged

@st.cache_data
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
