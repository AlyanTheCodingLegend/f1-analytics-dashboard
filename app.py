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
    _drivers_meta = data_loader.load_data('drivers.csv')
    _constructors_meta = data_loader.load_data('constructors.csv')
    _circuits_meta = data_loader.load_data('circuits.csv')

    _all_years = sorted(_races_meta['year'].unique().tolist()) if _races_meta is not None else list(range(1950, 2024))
    year_range = st.select_slider("Year Range", options=_all_years,
                                  value=(_all_years[0], _all_years[-1]))

    _driver_opts = sorted(_drivers_meta['surname'].dropna().unique().tolist()) if _drivers_meta is not None else []
    selected_drivers_global = st.multiselect("Drivers", _driver_opts,
                                             help="Leave empty to include all drivers")

    _team_opts = sorted(_constructors_meta['name'].dropna().unique().tolist()) if _constructors_meta is not None else []
    selected_teams_global = st.multiselect("Teams / Constructors", _team_opts,
                                           help="Leave empty to include all teams")

    _circuit_opts = sorted(_circuits_meta['name'].dropna().unique().tolist()) if _circuits_meta is not None else []
    selected_circuits_global = st.multiselect("Circuits", _circuit_opts,
                                              help="Leave empty to include all circuits")

    st.caption("ℹ️ Filters apply to pages that support them (Evolution of Speed, Dominance Dynasties, Championship Battle, Sprint Races).")

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
    st.write("F1 History is defined by eras of domination. This chart visualizes the *share* of total championship points scored by each team, accounting for changes in scoring systems over time.")

    dom_df = data_loader.get_dominance_data()

    if dom_df is not None:
        dom_df = dom_df[(dom_df['year'] >= year_range[0]) & (dom_df['year'] <= year_range[1])]

        if selected_teams_global:
            top_teams = [t for t in selected_teams_global if t in dom_df['name'].unique()]
            if not top_teams:
                top_teams = dom_df.groupby('name')['points'].sum().sort_values(ascending=False).head(10).index.tolist()
        else:
            top_teams = dom_df.groupby('name')['points'].sum().sort_values(ascending=False).head(10).index.tolist()

        dom_df['Team'] = dom_df['name'].apply(lambda x: x if x in top_teams else 'Others')
        chart_df = dom_df.groupby(['year', 'Team'])['points_share'].sum().reset_index()

        fig_area = px.area(chart_df, x='year', y='points_share', color='Team',
                           title='Constructor Dominance: Share of Championship Points per Year',
                           labels={'points_share': 'Share of Total Points (%)'},
                           category_orders={"Team": top_teams + ["Others"]})
        st.plotly_chart(fig_area, width="stretch")

        st.markdown("""
        **Key Dynasties Detected:**
        *   **Ferrari (Red):** The constant presence, peaking in the early 2000s (Schumacher Era).
        *   **McLaren (Orange/Silver):** Huge peaks in late 80s (Senna/Prost) and late 90s.
        *   **Williams (Blue):** Dominant in the 90s.
        *   **Red Bull:** The late 2010s/early 2020s surge.
        *   **Mercedes:** The massive hybrid-era domination (2014-2020).
        """)

        st.subheader("Race-by-Race Constructor Points")
        con_res_df = data_loader.get_constructor_results_data()
        if con_res_df is not None:
            available_seasons = sorted(con_res_df['year'].unique(), reverse=True)
            sel_season = st.selectbox("Select Season", available_seasons, key="dom_con_season")
            season_data = con_res_df[con_res_df['year'] == sel_season].copy()

            if selected_teams_global:
                show_teams = [t for t in selected_teams_global if t in season_data['name_team'].unique()]
            else:
                show_teams = season_data.groupby('name_team')['points'].sum().nlargest(8).index.tolist()
            season_data = season_data[season_data['name_team'].isin(show_teams)]
            season_data = season_data.sort_values('round')
            season_data['cumulative_points'] = season_data.groupby('name_team')['points'].cumsum()

            fig_rr = px.line(season_data, x='round', y='cumulative_points', color='name_team',
                             title=f"{sel_season} Constructor Points — Race by Race",
                             labels={'cumulative_points': 'Cumulative Points', 'round': 'Round', 'name_team': 'Constructor'},
                             markers=True)
            st.plotly_chart(fig_rr, width="stretch")
    else:
        st.error("Failed to load dominance data.")

elif page == "Geography of Victory":
    st.header("🌍 The Geography of Victory")
    st.write("Where do F1 champions come from? This map visualizes the total number of Grand Prix wins achieved by drivers from each country.")

    geo_df = data_loader.get_geography_data()

    if geo_df is not None:
        fig_map = px.choropleth(geo_df, locations="country", locationmode="country names",
                                color="wins", hover_name="nationality",
                                color_continuous_scale=px.colors.sequential.Plasma,
                                title="Total F1 Wins by Country of Driver Origin",
                                labels={'wins': 'Total Wins'})
        st.plotly_chart(fig_map, width="stretch")

        st.subheader("Leaderboard: Wins by Nation")
        st.dataframe(geo_df.sort_values(by='wins', ascending=False).set_index('country')[['wins']], width="stretch")

        st.markdown("""
        **Insights:**
        *   **United Kingdom:** Historically the most successful nation (Hamilton, Mansell, Stewart, Clark).
        *   **Germany:** Propelled largely by Michael Schumacher and Sebastian Vettel.
        *   **Brazil:** The legacy of Senna, Piquet, and Fittipaldi.
        *   **Finland:** The "Flying Finns" punch significantly above their weight relative to population size.
        """)
    else:
        st.error("Failed to load geography data.")

elif page == "Advanced: Quali vs Race":
    st.header("🚦 Qualifying Merchants vs. Race Monsters")
    st.write("This chart exposes the truth: Who falls back on Sunday, and who comes alive? We compare Average Grid Position vs. Average Finishing Position for experienced drivers (>50 races).")

    qvr_df = data_loader.get_quali_vs_race_data()

    if qvr_df is not None:
        fig_qvr = px.scatter(qvr_df, x='avg_grid', y='avg_finish',
                             title="Avg Grid Position vs. Avg Finishing Position",
                             labels={'avg_grid': 'Average Starting Position', 'avg_finish': 'Average Finishing Position', 'net_gain': 'Places Gained/Lost'},
                             hover_name='surname', hover_data=['races', 'code'],
                             color='net_gain',
                             color_continuous_scale=px.colors.diverging.RdYlGn,
                             color_continuous_midpoint=0)

        min_val = min(qvr_df['avg_grid'].min(), qvr_df['avg_finish'].min())
        max_val = max(qvr_df['avg_grid'].max(), qvr_df['avg_finish'].max())

        fig_qvr.add_shape(type="line",
            x0=min_val, y0=min_val, x1=max_val, y1=max_val,
            line=dict(color="Red", width=2, dash="dash"),
        )
        fig_qvr.add_annotation(x=max_val-2, y=max_val-5, text="Race Monsters (Gain Places)", showarrow=False, font=dict(color="green"))
        fig_qvr.add_annotation(x=max_val-5, y=max_val-2, text="Quali Merchants (Lose Places)", showarrow=False, font=dict(color="red"))
        fig_qvr.update_yaxes(autorange="reversed")
        fig_qvr.update_xaxes(autorange="reversed")
        st.plotly_chart(fig_qvr, width="stretch")
        st.markdown("**Interpretation**: Drivers below/left of the dashed line consistently improve their position on race day.")

elif page == "Advanced: Reliability":
    st.header("☠️ The Graveyard of Gears")
    st.write("Coming soon.")

elif page == "Advanced: Teammate Wars":
    st.header("⚔️ Teammate Killers")
    st.write("Compare legendary rivalries. Who came out on top in the same machinery?")

    rivalries = {
        "Hamilton vs Rosberg (Merc)": ("HAM", "ROS"),
        "Senna vs Prost (McLaren)": ("SEN", "PRO"),
        "Vettel vs Webber (Red Bull)": ("VET", "WEB"),
        "Verstappen vs Perez (Red Bull)": ("VER", "PER"),
        "Leclerc vs Sainz (Ferrari)": ("LEC", "SAI"),
        "Alonso vs Hamilton (McLaren 2007)": ("ALO", "HAM")
    }

    selection = st.selectbox("Select Rivalry", list(rivalries.keys()))
    d1_code, d2_code = rivalries[selection]

    stats = data_loader.get_teammate_comparison_data(d1_code, d2_code)

    if stats:
        st.subheader(f"{stats['d1_name']} vs {stats['d2_name']}")
        st.markdown(f"**Races Together:** {stats['races_together']}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"{stats['d1_name']} Wins", value=stats['d1_wins'])
            st.metric(label=f"{stats['d1_name']} Points", value=stats['d1_points'])
            st.metric(label="Finished Ahead", value=stats['d1_ahead'])
        with col2:
            st.metric(label=f"{stats['d2_name']} Wins", value=stats['d2_wins'])
            st.metric(label=f"{stats['d2_name']} Points", value=stats['d2_points'])
            st.metric(label="Finished Ahead", value=stats['d2_ahead'])

        comp_data = pd.DataFrame({
            'Driver': [stats['d1_name'], stats['d2_name']],
            'Points': [stats['d1_points'], stats['d2_points']],
            'Wins': [stats['d1_wins'], stats['d2_wins']]
        })
        fig_comp = px.bar(comp_data, x='Driver', y=['Points', 'Wins'], barmode='group', title="Head-to-Head Stats")
        st.plotly_chart(fig_comp, width="stretch")
    else:
        st.error("Data not found for these drivers.")

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
    st.header("🎯 The Underdog Effect: Can Strategy Overcome Speed?")
    st.write("""**The Ultimate Question**: If you start from the back of the grid, can brilliant strategy,
    tire management, and racecraft overcome a slow car? Let's find out.""")

    result = data_loader.get_underdog_analysis()

    if result is not None:
        base, underdogs = result

        st.subheader("1. The Comeback Kings (Biggest Position Gains)")
        top_comebacks = base.nlargest(20, 'positions_gained')[['year', 'surname', 'name_driver', 'grid', 'positionOrder', 'positions_gained', 'stops', 'lap_time_std']]
        fig_comeback = px.bar(top_comebacks, x='surname', y='positions_gained',
                              hover_data=['year', 'name_driver', 'grid', 'positionOrder'],
                              title="Top 20 Single-Race Comebacks (2011-2023)",
                              color='positions_gained', color_continuous_scale='Viridis',
                              labels={'positions_gained': 'Positions Gained', 'surname': 'Driver'})
        st.plotly_chart(fig_comeback, width="stretch")

        st.subheader("2. Does Strategy Matter More for Underdogs?")
        fig_box = px.box(base, x='grid_category', y='positions_gained',
                         title="Position Gains by Starting Grid Category",
                         category_orders={'grid_category': ['Front Row', 'Top 10', 'Midfield', 'Back Markers']},
                         color='grid_category',
                         labels={'positions_gained': 'Positions Gained', 'grid_category': 'Starting Position'})
        st.plotly_chart(fig_box, width="stretch")

        st.subheader("3. The Underdog Hall of Fame")
        underdog_stats = underdogs.groupby('surname').agg({
            'positions_gained': 'mean', 'raceId': 'count',
            'strategy_score': 'mean', 'stops': 'mean'
        }).reset_index()
        underdog_stats.columns = ['Driver', 'Avg Positions Gained', 'Underdog Races', 'Strategy Score', 'Avg Stops']
        underdog_stats = underdog_stats[underdog_stats['Underdog Races'] >= 5].sort_values('Avg Positions Gained', ascending=False).head(15)
        fig_underdog = px.scatter(underdog_stats, x='Avg Positions Gained', y='Strategy Score',
                                  size='Underdog Races', hover_data=['Driver', 'Avg Stops'],
                                  title="The Strategic Geniuses (Min. 5 Underdog Races)", text='Driver')
        st.plotly_chart(fig_underdog, width="stretch")

        st.subheader("4. The Pit Stop Gamble")
        back_starters = base[base['grid'] > 10].copy()
        pit_analysis = back_starters.groupby('stops')['positions_gained'].mean().reset_index()
        pit_analysis = pit_analysis[pit_analysis['stops'] <= 5]
        fig_pit = px.line(pit_analysis, x='stops', y='positions_gained',
                          title="Average Position Gain vs. Number of Pit Stops (Started 11th+)",
                          markers=True, labels={'stops': 'Number of Pit Stops', 'positions_gained': 'Avg Positions Gained'})
        st.plotly_chart(fig_pit, width="stretch")
    else:
        st.error("Could not load Underdog Analysis data.")

elif page == "⚰️ THE CONSTRUCTOR'S CURSE":
    st.header("⚰️ The Constructor's Curse: Why Dynasties Fall")
    st.write("""**The Inevitable Truth**: Every F1 dynasty eventually crumbles.
    Can we predict when the current champions will fall? Let's analyze the warning signs.""")

    result = data_loader.get_dynasty_decline_analysis()

    if result is not None:
        yearly_stats, dynasty_data = result

        st.subheader("1. The Rise and Fall of Empires")
        dynasties_to_plot = ['Ferrari', 'McLaren', 'Red Bull', 'Mercedes', 'Williams']
        dynasty_subset = dynasty_data[dynasty_data['constructor'].isin(dynasties_to_plot)]
        fig_lifecycle = px.line(dynasty_subset, x='year', y='market_share', color='constructor',
                                title="Market Share Over Time: The Great Dynasties (1950-2023)",
                                labels={'market_share': 'Market Share (%)', 'year': 'Year', 'constructor': 'Team'},
                                markers=True)
        fig_lifecycle.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Dominance Threshold (20%)")
        st.plotly_chart(fig_lifecycle, width="stretch")

        st.subheader("2. The Warning Signs of Decline")
        recent_dynasties = dynasty_data[dynasty_data['year'] >= 2010]
        fig_decline = px.scatter(recent_dynasties, x='year', y='constructor',
                                 size='market_share', color='decline_score',
                                 title="Decline Warning Signals (2010-2023)",
                                 color_continuous_scale='RdYlGn_r',
                                 labels={'decline_score': 'Warning Level', 'market_share': 'Market Share'})
        st.plotly_chart(fig_decline, width="stretch")

        st.subheader("3. How Fast Do Dynasties Fall?")
        collapse_analysis = []
        for team in dynasties_to_plot:
            team_data = dynasty_data[dynasty_data['constructor'] == team].sort_values('year')
            peaks = team_data[team_data['market_share'] > 30]
            if not peaks.empty:
                for _, peak_row in peaks.iterrows():
                    peak_year = peak_row['year']
                    future_data = team_data[team_data['year'] > peak_year]
                    trough = future_data[future_data['market_share'] < 10]
                    if not trough.empty:
                        trough_year = trough.iloc[0]['year']
                        collapse_analysis.append({'Team': team, 'Peak Year': peak_year, 'Collapse Year': trough_year, 'Years to Collapse': trough_year - peak_year})

        if collapse_analysis:
            collapse_df = pd.DataFrame(collapse_analysis)
            fig_collapse = px.bar(collapse_df, x='Team', y='Years to Collapse',
                                  hover_data=['Peak Year', 'Collapse Year'],
                                  title="Time from Peak Dominance to Irrelevance",
                                  color='Years to Collapse', color_continuous_scale='Reds')
            st.plotly_chart(fig_collapse, width="stretch")
            st.metric("Average Collapse Duration", f"{collapse_df['Years to Collapse'].mean():.1f} years")

        st.subheader("4. Who's Next to Fall?")
        recent_data = dynasty_data[dynasty_data['year'] >= 2021].copy()
        current_status = recent_data.groupby('constructor').agg({
            'market_share': 'mean', 'points_pct_change': 'mean',
            'decline_score': 'mean', 'reliability': 'mean'
        }).reset_index().sort_values('market_share', ascending=False).head(5)
        fig_current = px.bar(current_status, x='constructor', y='market_share', color='decline_score',
                             title="Current Dynasty Health Check (2021-2023 Average)",
                             color_continuous_scale='RdYlGn_r',
                             labels={'market_share': 'Avg Market Share (%)', 'constructor': 'Team', 'decline_score': 'Risk Level'})
        st.plotly_chart(fig_current, width="stretch")
    else:
        st.error("Could not load Dynasty Analysis data.")

elif page == "🧒 THE ROOKIE PARADOX":
    st.header("🧒 The Rookie Paradox: When Experience Becomes a Curse")
    st.write("""**The Burning Question**: At what age do F1 drivers peak?
    And when does experience stop helping and start hurting? Let's find the sweet spot.""")

    result = data_loader.get_rookie_paradox_analysis()

    if result is not None:
        base, driver_stats = result

        st.subheader("1. The Biological Clock: Age vs. Performance")
        age_performance = base.groupby('age_group')['positionOrder'].mean().reset_index().sort_values('positionOrder')
        fig_age = px.bar(age_performance, x='age_group', y='positionOrder',
                         title="Average Finishing Position by Age Group",
                         labels={'positionOrder': 'Avg Finish Position', 'age_group': 'Age Group'},
                         color='positionOrder', color_continuous_scale='RdYlGn_r')
        fig_age.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_age, width="stretch")
        st.success(f"🎯 **Peak Performance Age**: {age_performance.iloc[0]['age_group']}")

        st.subheader("2. The Learning Curve: Experience vs. Results")
        exp_order = ['Rookie (1-20 races)', 'Developing (21-50)', 'Experienced (51-100)', 'Veteran (101-200)', 'Legend (200+)']
        exp_performance = base.groupby('experience_level').agg({'positionOrder': 'mean', 'podium': 'mean', 'points_scored': 'mean'}).reset_index()
        exp_performance['experience_level'] = pd.Categorical(exp_performance['experience_level'], categories=exp_order, ordered=True)
        exp_performance = exp_performance.sort_values('experience_level')
        fig_learning = px.line(exp_performance, x='experience_level', y='positionOrder',
                               title="The Learning Curve: Performance by Experience Level",
                               labels={'positionOrder': 'Avg Finish Position', 'experience_level': 'Experience'}, markers=True)
        fig_learning.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_learning, width="stretch")

        st.subheader("3. The Podium Probability Matrix")
        age_order = ['Young Gun (<23)', 'Prime (23-27)', 'Experienced (28-32)', 'Veteran (33-37)', 'Elder (38+)']
        podium_matrix = base.groupby(['age_group', 'experience_level'])['podium'].mean().reset_index()
        podium_pivot = podium_matrix.pivot(index='age_group', columns='experience_level', values='podium')
        podium_pivot = podium_pivot.reindex(age_order)
        podium_pivot = podium_pivot.reindex(columns=exp_order)
        fig_matrix = px.imshow(podium_pivot, title="Podium Probability by Age and Experience (%)",
                               color_continuous_scale='YlOrRd', text_auto='.2%')
        st.plotly_chart(fig_matrix, width="stretch")
    else:
        st.error("Could not load Rookie Paradox data.")

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
