import streamlit as st
import data_loader
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Formula 1 Data Visualization",
    page_icon="🏎️",
    layout="wide"
)

# Title
st.title("🏎️ Formula 1 Analytics Dashboard")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Evolution of Speed",
    "Dominance Dynasties",
    "Geography of Victory",
    "Advanced: Quali vs Race",
    "Advanced: Reliability",
    "Advanced: Teammate Wars",
    "🏆 Championship Battle",
    "⚡ Sprint Races",
    "THE WINNING FORMULA 🏆",
    "🎯 THE UNDERDOG EFFECT",
    "⚰️ THE CONSTRUCTOR'S CURSE",
    "🧒 THE ROOKIE PARADOX",
    "🏎️ THE CIRCUIT DNA",
    "💰 THE MILLION DOLLAR LAP",
    "🦋 THE BUTTERFLY EFFECT",
    "🌈 THE RAINBOW ROAD",
    "⛈️ THE PERFECT STORM"
])

# --- Global Filters (placeholder — filters wired in later) ---
st.sidebar.markdown("---")
with st.sidebar.expander("🔍 Global Filters", expanded=False):
    _races_meta = data_loader.load_data('races.csv')
    _all_years = sorted(_races_meta['year'].unique().tolist()) if _races_meta is not None else list(range(1950, 2024))
    year_range = st.select_slider("Year Range", options=_all_years, value=(_all_years[0], _all_years[-1]))
    selected_drivers_global = []
    selected_teams_global = []
    selected_circuits_global = []
    st.caption("ℹ️ Year filter applies to Evolution of Speed and Championship Battle.")

# Page routing
if page == "Home":
    st.write("### Welcome to the Formula 1 History Analyzer")
    st.write("This dashboard explores the rich history of F1 through three key lenses:")
    st.markdown("- **The Evolution of Speed**: How cars and circuits have changed.")
    st.markdown("- **Dominance Dynasties**: The rise and fall of great teams.")
    st.markdown("- **The Geography of Victory**: Where champions come from and where they win.")
    st.info("Select a page from the sidebar to begin exploring.")

    # Dataset overview using seasons.csv
    overview = data_loader.get_seasons_overview()
    if overview is not None:
        st.markdown("---")
        st.subheader("📊 Dataset at a Glance")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Seasons", overview['total_seasons'],
                  f"{overview['year_range'][0]}–{overview['year_range'][1]}")
        c2.metric("Races", overview['total_races'])
        c3.metric("Drivers", overview['total_drivers'])
        c4.metric("Circuits", overview['total_circuits'])

        st.subheader("📅 F1 Calendar Growth Over the Decades")
        fig_cal = px.line(overview['races_per_year'], x='year', y='race_count',
                          title="Number of Races per Season (1950–2023)",
                          labels={'race_count': 'Races', 'year': 'Year'},
                          markers=True)
        fig_cal.update_traces(line_color='#e10600')
        st.plotly_chart(fig_cal, width="stretch")

elif page == "Evolution of Speed":
    st.header("🏎️ The Evolution of Speed")
    st.write("Does F1 really get faster every year? Let's analyze the `fastestLapSpeed` recorded in races over the decades.")

    speed_df = data_loader.get_speed_data()

    if speed_df is not None:
        speed_df = speed_df[(speed_df['year'] >= year_range[0]) & (speed_df['year'] <= year_range[1])]
        if selected_circuits_global:
            speed_df = speed_df[speed_df['name_circuit'].isin(selected_circuits_global)]

        st.subheader("Global Trend: Fastest Lap Speeds over Time")
        max_speed_per_year = speed_df.groupby('year')['fastestLapSpeed'].max().reset_index()
        fig_trend = px.line(max_speed_per_year, x='year', y='fastestLapSpeed',
                            title='Maximum Race Lap Speed Recorded by Year (km/h)',
                            markers=True, labels={'fastestLapSpeed': 'Speed (km/h)'})
        st.plotly_chart(fig_trend, width="stretch")
        st.markdown("**Observation:** Notice the dips? These often correlate with regulation changes (e.g., V10 to V8 engines, aero restrictions).")

        st.subheader("Circuit Specific Analysis")
        st.write("Compare speeds on specific tracks to verify if cars are getting faster on the same tarmac.")
        selected_circuits = st.multiselect("Select Circuits to Compare", speed_df['name_circuit'].unique(), default=['Circuit de Monaco', 'Autodromo Nazionale di Monza', 'Silverstone Circuit'])
        filtered_df = speed_df[speed_df['name_circuit'].isin(selected_circuits)]
        circuit_yearly_max = filtered_df.groupby(['year', 'name_circuit'])['fastestLapSpeed'].max().reset_index()
        fig_circuit = px.scatter(circuit_yearly_max, x='year', y='fastestLapSpeed', color='name_circuit',
                                 title='Max Speed Evolution by Circuit',
                                 trendline="lowess",
                                 labels={'fastestLapSpeed': 'Speed (km/h)'})
        st.plotly_chart(fig_circuit, width="stretch")
    else:
        st.error("Failed to load speed data. Please check the dataset.")

elif page == "Dominance Dynasties":
    st.header("🏆 Dominance Dynasties")
    st.write("Coming soon.")

elif page == "Geography of Victory":
    st.header("🌍 The Geography of Victory")
    st.write("Coming soon.")

elif page == "Advanced: Quali vs Race":
    st.header("🚦 Qualifying Merchants vs. Race Monsters")
    st.write("Coming soon.")

elif page == "Advanced: Reliability":
    st.header("☠️ The Graveyard of Gears")
    st.write("Coming soon.")

elif page == "Advanced: Teammate Wars":
    st.header("⚔️ Teammate Killers")
    st.write("Coming soon.")

elif page == "🏆 Championship Battle":
    st.header("🏆 Championship Battle: Season Standings Evolution")
    st.write("Watch how the Drivers' World Championship unfolded race by race, using the official standings data.")

    standings_df = data_loader.get_driver_standings_evolution()

    if standings_df is not None:
        available_years = sorted(
            [y for y in standings_df['year'].unique() if year_range[0] <= y <= year_range[1]],
            reverse=True
        )
        if not available_years:
            st.warning("No data for the selected year range. Adjust the Global Filters.")
        else:
            selected_year = st.selectbox("Select Season", available_years)
            year_data = standings_df[standings_df['year'] == selected_year].copy()

            if selected_drivers_global:
                year_data = year_data[year_data['surname'].isin(selected_drivers_global)]

            top_drivers = year_data.groupby('surname')['points'].max().nlargest(10).index.tolist()
            plot_data = year_data[year_data['surname'].isin(top_drivers)]

            st.subheader("Points Race: Round by Round")
            fig_battle = px.line(plot_data, x='round', y='points', color='surname',
                                 title=f"{selected_year} Drivers' Championship — Standings After Each Race",
                                 labels={'points': 'Cumulative Points', 'round': 'Race Round', 'surname': 'Driver'},
                                 markers=True)
            st.plotly_chart(fig_battle, width="stretch")
            st.info("💡 Each point represents the standings *after* that race. Lines crossing = lead changes!")

            st.subheader("Final Season Standings")
            final = year_data.groupby('surname')['points'].max().reset_index()
            final = final.sort_values('points', ascending=False).head(15)
            fig_final = px.bar(final, x='surname', y='points',
                               title=f"{selected_year} Final Driver Standings (Top 15)",
                               labels={'points': 'Championship Points', 'surname': 'Driver'},
                               color='points', color_continuous_scale='Plasma')
            st.plotly_chart(fig_final, width="stretch")

            st.subheader("Race Wins Tally")
            wins_data = year_data.groupby('surname')['wins'].max().reset_index()
            wins_data = wins_data[wins_data['wins'] > 0].sort_values('wins', ascending=False)
            if not wins_data.empty:
                fig_wins = px.bar(wins_data, x='surname', y='wins',
                                  title=f"{selected_year} Race Wins",
                                  labels={'wins': 'Wins', 'surname': 'Driver'},
                                  color='wins', color_continuous_scale='Reds')
                st.plotly_chart(fig_wins, width="stretch")

            st.subheader("Gap to Championship Leader")
            leader_points = plot_data.groupby('round')['points'].max().reset_index().rename(columns={'points': 'leader_pts'})
            gap_data = pd.merge(plot_data, leader_points, on='round')
            gap_data['gap'] = gap_data['leader_pts'] - gap_data['points']
            fig_gap = px.line(gap_data, x='round', y='gap', color='surname',
                              title=f"{selected_year} Points Gap to Championship Leader",
                              labels={'gap': 'Points Behind Leader', 'round': 'Race Round', 'surname': 'Driver'},
                              markers=True)
            st.plotly_chart(fig_gap, width="stretch")
            st.info("💡 Closer to zero = closer to the title. Zero = leading the championship at that point.")
    else:
        st.error("Could not load Championship Battle data.")

elif page == "⚡ Sprint Races":
    st.header("⚡ Sprint Races")
    st.write("Coming soon.")

elif page == "THE WINNING FORMULA 🏆":
    st.header("🏆 The Winning Formula")
    st.write("Coming soon.")

elif page == "🎯 THE UNDERDOG EFFECT":
    st.header("🎯 The Underdog Effect")
    st.write("Coming soon.")

elif page == "⚰️ THE CONSTRUCTOR'S CURSE":
    st.header("⚰️ The Constructor's Curse")
    st.write("Coming soon.")

elif page == "🧒 THE ROOKIE PARADOX":
    st.header("🧒 The Rookie Paradox")
    st.write("Coming soon.")

elif page == "🏎️ THE CIRCUIT DNA":
    st.header("🏎️ The Circuit DNA")
    st.write("Coming soon.")

elif page == "💰 THE MILLION DOLLAR LAP":
    st.header("💰 The Million Dollar Lap")
    st.write("Coming soon.")

elif page == "🦋 THE BUTTERFLY EFFECT":
    st.header("🦋 The Butterfly Effect")
    st.write("Coming soon.")

elif page == "🌈 THE RAINBOW ROAD":
    st.header("🌈 The Rainbow Road")
    st.write("Coming soon.")

elif page == "⛈️ THE PERFECT STORM":
    st.header("⛈️ The Perfect Storm")
    st.write("Coming soon.")
