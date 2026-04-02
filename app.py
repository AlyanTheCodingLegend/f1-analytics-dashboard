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

st.sidebar.markdown("---")
st.sidebar.info("🔍 Global filters coming soon.")

# Page routing — content to be added per page
if page == "Home":
    st.write("Home page — coming soon.")
elif page == "Evolution of Speed":
    st.write("Evolution of Speed — coming soon.")
elif page == "Dominance Dynasties":
    st.write("Dominance Dynasties — coming soon.")
elif page == "Geography of Victory":
    st.write("Geography of Victory — coming soon.")
elif page == "Advanced: Quali vs Race":
    st.write("Quali vs Race — coming soon.")
elif page == "Advanced: Reliability":
    st.write("Reliability — coming soon.")
elif page == "Advanced: Teammate Wars":
    st.write("Teammate Wars — coming soon.")
elif page == "🏆 Championship Battle":
    st.write("Championship Battle — coming soon.")
elif page == "⚡ Sprint Races":
    st.write("Sprint Races — coming soon.")
elif page == "THE WINNING FORMULA 🏆":
    st.write("The Winning Formula — coming soon.")
elif page == "🎯 THE UNDERDOG EFFECT":
    st.write("The Underdog Effect — coming soon.")
elif page == "⚰️ THE CONSTRUCTOR'S CURSE":
    st.write("The Constructor's Curse — coming soon.")
elif page == "🧒 THE ROOKIE PARADOX":
    st.write("The Rookie Paradox — coming soon.")
elif page == "🏎️ THE CIRCUIT DNA":
    st.write("Circuit DNA — coming soon.")
elif page == "💰 THE MILLION DOLLAR LAP":
    st.write("The Million Dollar Lap — coming soon.")
elif page == "🦋 THE BUTTERFLY EFFECT":
    st.write("The Butterfly Effect — coming soon.")
elif page == "🌈 THE RAINBOW ROAD":
    st.write("The Rainbow Road — coming soon.")
elif page == "⛈️ THE PERFECT STORM":
    st.write("The Perfect Storm — coming soon.")
