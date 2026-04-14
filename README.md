# F1 Analytics Dashboard

An interactive Formula 1 data visualization dashboard built with Streamlit and Plotly.

## Overview

This dashboard explores the rich history of Formula 1 (1950–2023) through 18 analytical pages covering speed evolution, team dynasties, driver performance, circuit analysis, and more.

## Tech Stack

- **Python 3.10+**
- **Streamlit** — web app framework
- **Pandas** — data processing
- **Plotly** — interactive charts

## Dataset

13 CSV files sourced from the Ergast F1 dataset:
- `circuits.csv`, `constructors.csv`, `drivers.csv`, `races.csv`, `results.csv`
- `qualifying.csv`, `lap_times.csv`, `pit_stops.csv`, `sprint_results.csv`
- `driver_standings.csv`, `constructor_standings.csv`, `constructor_results.csv`, `seasons.csv`

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Team

| Member | Role |
|--------|------|
| Alyan Ahmed | Lead Developer & Scrum Master |
| Abeera Amir | Frontend / Navigation |
| Abdul Hadi Sheikh | Data Visualization |
| Abdullah Salim Nizami | Data Engineering |

## Pages

| Page | Description |
|------|-------------|
| Home | Dataset overview, season calendar growth |
| Evolution of Speed | Lap record trends, circuit speed scatter |
| Dominance Dynasties | Constructor points stacked area, race-by-race breakdown |
| Geography of Victory | Choropleth map of wins by country |
| Advanced: Quali vs Race | Qualifying vs finish position correlation |
| Advanced: Reliability | DNF rates by decade |
| Advanced: Teammate Wars | Head-to-head comparison metrics |
| Championship Battle | Race-by-race standings gap visualization |
| Sprint Races | Sprint win trends, grid vs finish analysis |
| THE WINNING FORMULA | Correlation heatmap, 3D strategy scatter |
| THE UNDERDOG EFFECT | Comeback analysis, pit stop gambles |
| THE CONSTRUCTOR'S CURSE | Team lifecycle and decline velocity |
| THE ROOKIE PARADOX | Age vs performance learning curve |
| THE CIRCUIT DNA | Track difficulty index, specialist heatmap |
| THE MILLION DOLLAR LAP | Budget efficiency vs championship success |
| THE BUTTERFLY EFFECT | Drama scores, clutch laps, fastest pit stops |
| THE RAINBOW ROAD | Sunburst, treemap, Sankey, 3D driver galaxy |
| THE PERFECT STORM | Perfect performances vs disasters, DNF causes |

## Sprint Timeline

- **Sprint 1 (Apr 1–7):** Data pipeline, navigation, core pages (Home, Speed, Championships)
- **Sprint 2 (Apr 8–14):** Advanced analytics — 11 thematic pages, full filter system, final polish
