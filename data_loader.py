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

@st.cache_data
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

def get_teammate_comparison_data(driver1_code, driver2_code, constructor_name=None):
    """
    Compares two drivers when they were teammates.
    """
    results = load_data('results.csv')
    drivers = load_data('drivers.csv')
    constructors = load_data('constructors.csv')
    races = load_data('races.csv')

    d1 = drivers[drivers['code'] == driver1_code]
    d2 = drivers[drivers['code'] == driver2_code]

    if d1.empty or d2.empty:
        return None

    d1_id = d1.iloc[0]['driverId']
    d2_id = d2.iloc[0]['driverId']

    r1 = results[results['driverId'] == d1_id][['raceId', 'constructorId', 'points', 'positionOrder']]
    r2 = results[results['driverId'] == d2_id][['raceId', 'constructorId', 'points', 'positionOrder']]

    teammates = pd.merge(r1, r2, on=['raceId', 'constructorId'], suffixes=('_1', '_2'))
    final_df = pd.merge(teammates, races[['raceId', 'year', 'name']], on='raceId')

    stats = {
        'd1_wins': len(final_df[final_df['positionOrder_1'] == 1]),
        'd2_wins': len(final_df[final_df['positionOrder_2'] == 1]),
        'd1_points': final_df['points_1'].sum(),
        'd2_points': final_df['points_2'].sum(),
        'd1_ahead': len(final_df[final_df['positionOrder_1'] < final_df['positionOrder_2']]),
        'd2_ahead': len(final_df[final_df['positionOrder_2'] < final_df['positionOrder_1']]),
        'races_together': len(final_df),
        'd1_name': d1.iloc[0]['surname'],
        'd2_name': d2.iloc[0]['surname']
    }

    return stats

def get_unified_data():
    """
    Builds the Master DataFrame for 'The Winning Formula' analysis.
    Merges: Results, Qualifying, Lap Times (Aggregated), Pit Stops (Aggregated).
    """
    results = load_data('results.csv')
    races = load_data('races.csv')
    drivers = load_data('drivers.csv')
    constructors = load_data('constructors.csv')
    qualifying = load_data('qualifying.csv')
    pit_stops = load_data('pit_stops.csv')
    lap_times = load_data('lap_times.csv')

    if any(df is None for df in [results, races, drivers, constructors, qualifying, pit_stops, lap_times]):
        return None

    base = pd.merge(results, races[['raceId', 'year', 'name', 'circuitId']], on='raceId', suffixes=('_res', '_race'))
    base = pd.merge(base, drivers[['driverId', 'code', 'surname', 'nationality']], on='driverId')
    base = pd.merge(base, constructors[['constructorId', 'name']], on='constructorId', suffixes=('_driver', '_team'))
    base = base[base['year'] >= 2011].copy()

    quali_subset = qualifying[['raceId', 'driverId', 'position']].rename(columns={'position': 'quali_pos'})
    base = pd.merge(base, quali_subset, on=['raceId', 'driverId'], how='left')

    pit_agg = pit_stops.groupby(['raceId', 'driverId']).agg({
        'stop': 'max',
        'milliseconds': 'sum'
    }).reset_index().rename(columns={'stop': 'stops', 'milliseconds': 'total_pit_time'})
    pit_agg['total_pit_time'] = pit_agg['total_pit_time'] / 1000
    base = pd.merge(base, pit_agg, on=['raceId', 'driverId'], how='left')
    base['stops'] = base['stops'].fillna(0)
    base['total_pit_time'] = base['total_pit_time'].fillna(0)

    relevant_races = base['raceId'].unique()
    laps_subset = lap_times[lap_times['raceId'].isin(relevant_races)]
    lap_agg = laps_subset.groupby(['raceId', 'driverId'])['milliseconds'].agg(['std', 'mean']).reset_index()
    lap_agg = lap_agg.rename(columns={'std': 'lap_time_std', 'mean': 'avg_lap_time'})
    base = pd.merge(base, lap_agg, on=['raceId', 'driverId'], how='left')

    base['Win'] = base['positionOrder'].apply(lambda x: 1 if x == 1 else 0)
    base['Podium'] = base['positionOrder'].apply(lambda x: 1 if x <= 3 else 0)

    return base

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

def get_dynasty_decline_analysis():
    """
    Analyzes 'The Constructor's Curse': Why do dominant teams eventually fall?
    """
    results = load_data('results.csv')
    races = load_data('races.csv')
    constructors = load_data('constructors.csv')
    constructor_standings = load_data('constructor_standings.csv')

    if any(df is None for df in [results, races, constructors, constructor_standings]):
        return None

    base = pd.merge(results, races[['raceId', 'year']], on='raceId')
    base = pd.merge(base, constructors[['constructorId', 'name']], on='constructorId')

    yearly_stats = base.groupby(['year', 'name']).agg({
        'points': 'sum',
        'positionOrder': 'mean',
        'statusId': lambda x: (x == 1).sum() / len(x)
    }).reset_index()
    yearly_stats.columns = ['year', 'constructor', 'total_points', 'avg_finish', 'reliability']

    yearly_stats = yearly_stats.sort_values(['constructor', 'year'])
    yearly_stats['points_change'] = yearly_stats.groupby('constructor')['total_points'].diff()
    yearly_stats['points_pct_change'] = yearly_stats.groupby('constructor')['total_points'].pct_change() * 100
    yearly_stats['total_season_points'] = yearly_stats.groupby('year')['total_points'].transform('sum')
    yearly_stats['market_share'] = (yearly_stats['total_points'] / yearly_stats['total_season_points']) * 100
    yearly_stats['is_dominant'] = yearly_stats['market_share'] > 20

    dynasties = ['Ferrari', 'McLaren', 'Red Bull', 'Mercedes', 'Williams', 'Renault']
    dynasty_data = yearly_stats[yearly_stats['constructor'].isin(dynasties)].copy()

    dynasty_data['decline_score'] = 0
    dynasty_data.loc[dynasty_data['points_pct_change'] < -10, 'decline_score'] += 1
    dynasty_data.loc[dynasty_data['reliability'] < 0.7, 'decline_score'] += 1
    dynasty_data.loc[dynasty_data['avg_finish'] > 8, 'decline_score'] += 1

    return yearly_stats, dynasty_data

def get_geography_data():
    """
    Prepares data for 'The Geography of Victory'.
    Counts wins per driver nationality.
    """
    results = load_data('results.csv')
    drivers = load_data('drivers.csv')

    if results is None or drivers is None:
        return None

    merged = pd.merge(results, drivers, on='driverId')
    wins = merged[merged['positionOrder'] == 1]
    win_counts = wins['nationality'].value_counts().reset_index()
    win_counts.columns = ['nationality', 'wins']

    nationality_map = {
        'British': 'United Kingdom', 'German': 'Germany', 'Brazilian': 'Brazil',
        'French': 'France', 'Finnish': 'Finland', 'Italian': 'Italy',
        'Australian': 'Australia', 'Austrian': 'Austria', 'Argentine': 'Argentina',
        'American': 'United States', 'Canadian': 'Canada', 'Spanish': 'Spain',
        'Dutch': 'Netherlands', 'Belgian': 'Belgium', 'Swedish': 'Sweden',
        'New Zealander': 'New Zealand', 'South African': 'South Africa',
        'Swiss': 'Switzerland', 'Colombian': 'Colombia', 'Venezuelan': 'Venezuela',
        'Mexican': 'Mexico', 'Polish': 'Poland', 'Monegasque': 'Monaco'
    }
    win_counts['country'] = win_counts['nationality'].map(nationality_map).fillna(win_counts['nationality'])

    return win_counts

def get_reliability_data():
    """
    Prepares data for 'The Graveyard of Gears' (Reliability evolution).
    """
    results = load_data('results.csv')
    status = load_data('status.csv')
    races = load_data('races.csv')

    if results is None or status is None or races is None:
        return None

    merged = pd.merge(results, status, on='statusId')
    merged = pd.merge(merged, races[['raceId', 'year']], on='raceId')

    def categorize_status(row):
        sid = row['statusId']
        s = row['status'].lower()
        if sid == 1 or s.startswith('+'): return 'Finished'
        elif sid in [3, 4, 130, 137] or 'accident' in s or 'collision' in s or 'spun' in s: return 'Accident/Collision'
        elif sid == 2 or 'disqualified' in s: return 'Disqualified'
        else: return 'Mechanical/Technical Failure'

    merged['category'] = merged.apply(categorize_status, axis=1)
    merged['decade'] = (merged['year'] // 10) * 10
    merged['decade'] = merged['decade'].astype(str) + "s"

    agg = merged.groupby(['decade', 'category']).size().reset_index(name='count')
    decade_totals = agg.groupby('decade')['count'].transform('sum')
    agg['percentage'] = (agg['count'] / decade_totals) * 100

    return agg

def get_rookie_paradox_analysis():
    """
    Analyzes 'The Rookie Paradox': When does experience become a curse?
    """
    results = load_data('results.csv')
    races = load_data('races.csv')
    drivers = load_data('drivers.csv')

    if any(df is None for df in [results, races, drivers]):
        return None

    base = pd.merge(results, races[['raceId', 'year', 'date']], on='raceId')
    base = pd.merge(base, drivers[['driverId', 'code', 'surname', 'dob']], on='driverId')

    base['date'] = pd.to_datetime(base['date'])
    base['dob'] = pd.to_datetime(base['dob'])
    base['age'] = (base['date'] - base['dob']).dt.days / 365.25

    base = base.sort_values(['driverId', 'date'])
    base['race_number'] = base.groupby('driverId').cumcount() + 1

    def experience_category(race_num):
        if race_num <= 20: return 'Rookie (1-20 races)'
        elif race_num <= 50: return 'Developing (21-50)'
        elif race_num <= 100: return 'Experienced (51-100)'
        elif race_num <= 200: return 'Veteran (101-200)'
        else: return 'Legend (200+)'

    def age_category(age):
        if age < 23: return 'Young Gun (<23)'
        elif age < 28: return 'Prime (23-27)'
        elif age < 33: return 'Experienced (28-32)'
        elif age < 38: return 'Veteran (33-37)'
        else: return 'Elder (38+)'

    base['experience_level'] = base['race_number'].apply(experience_category)
    base['age_group'] = base['age'].apply(age_category)
    base['podium'] = (base['positionOrder'] <= 3).astype(int)
    base['points_scored'] = base['points'] > 0

    driver_stats = base.groupby('driverId').agg({
        'age': 'mean', 'race_number': 'max', 'positionOrder': 'mean',
        'points': 'sum', 'podium': 'sum', 'surname': 'first'
    }).reset_index()
    driver_stats = driver_stats[driver_stats['race_number'] >= 50]

    return base, driver_stats

def get_underdog_analysis():
    """
    Analyzes 'The Underdog Effect': Can strategy overcome poor qualifying?
    """
    base = get_unified_data()

    if base is None:
        return None

    base['positions_gained'] = base['grid'] - base['positionOrder']
    base['quali_deficit'] = base['quali_pos'] - 1

    def categorize_grid(grid):
        if grid <= 3:
            return 'Front Row'
        elif grid <= 10:
            return 'Top 10'
        elif grid <= 15:
            return 'Midfield'
        else:
            return 'Back Markers'

    base['grid_category'] = base['grid'].apply(categorize_grid)

    underdogs = base[(base['grid'] > 5) & (base['positionOrder'] <= 10)].copy()
    underdogs['strategy_score'] = (
        (underdogs['stops'].clip(1, 4) / 4) * 0.3 +
        (1 / (underdogs['lap_time_std'].fillna(underdogs['lap_time_std'].mean()) / 1000)) * 0.7
    )

    return base, underdogs

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
