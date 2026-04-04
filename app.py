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
    st.caption("ℹ️ Year filter active. Driver/team/circuit filters coming in Sprint 2.")

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

        st.subheader("F1 Calendar Growth")
        fig_cal = px.line(overview['races_per_year'], x='year', y='race_count',
                          title="Number of Races per Season",
                          labels={'race_count': 'Races', 'year': 'Year'},
                          markers=True)
        st.plotly_chart(fig_cal, width="stretch")

elif page == "Evolution of Speed":
    st.header("🏎️ The Evolution of Speed")
    st.write(f"Showing data from {year_range[0]} to {year_range[1]}. Full charts coming soon.")

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
    st.header("🏆 Championship Battle")
    st.write("Coming soon.")

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
