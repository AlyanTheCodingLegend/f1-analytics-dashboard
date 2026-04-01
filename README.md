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

## Sprint Timeline

- **Sprint 1 (Apr 1–7):** Data pipeline, navigation, core pages
- **Sprint 2 (Apr 8–14):** Advanced analytics, full dashboard
