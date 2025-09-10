#!/usr/bin/env python3
"""
Fantasy Football 2025 Dashboard
Main Streamlit application for fantasy football league analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="Fantasy Football 2025 Dashboard",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🏈 Fantasy Football 2025 League Dashboard")
st.markdown("---")

# Sidebar configuration
st.sidebar.title("Dashboard Configuration")

# Load league configuration if it exists
config_path = os.path.join("config", "league_config.json")
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        league_config = json.load(f)
        league_name = league_config.get("league_name", "My Fantasy League")
        teams_count = league_config.get("teams_count", 12)
else:
    league_name = "My Fantasy League"
    teams_count = 12

st.sidebar.write(f"**League:** {league_name}")
st.sidebar.write(f"**Teams:** {teams_count}")

# Navigation
page = st.sidebar.selectbox(
    "Navigate to:",
    ["Overview", "Team Analysis", "Player Stats", "Matchup Predictor", "Waiver Wire"]
)

# Sample data for demonstration
@st.cache_data
def load_sample_data():
    """Load sample fantasy football data"""
    # Create sample team data
    teams_data = {
        'Team': [f'Team {i+1}' for i in range(teams_count)],
        'Owner': [f'Owner {i+1}' for i in range(teams_count)],
        'Wins': [7, 6, 8, 5, 9, 4, 7, 6, 5, 8, 3, 6][:teams_count],
        'Losses': [6, 7, 5, 8, 4, 9, 6, 7, 8, 5, 10, 7][:teams_count],
        'Points For': [1245.5, 1189.2, 1298.7, 1087.3, 1356.8, 1021.4, 1234.6, 1156.7, 1098.2, 1267.9, 967.3, 1201.5][:teams_count],
        'Points Against': [1198.3, 1234.5, 1167.8, 1278.9, 1089.6, 1298.7, 1201.2, 1189.4, 1245.6, 1156.3, 1289.7, 1178.9][:teams_count]
    }
    
    # Create sample player data
    players_data = {
        'Player': ['Josh Allen', 'Christian McCaffrey', 'Cooper Kupp', 'Travis Kelce', 'Derrick Henry'],
        'Position': ['QB', 'RB', 'WR', 'TE', 'RB'],
        'Team': ['BUF', 'SF', 'LAR', 'KC', 'TEN'],
        'Points': [287.4, 234.6, 189.3, 156.7, 198.2],
        'Games': [13, 11, 9, 13, 12],
        'Avg Points': [22.1, 21.3, 21.0, 12.1, 16.5]
    }
    
    return pd.DataFrame(teams_data), pd.DataFrame(players_data)

# Load data
teams_df, players_df = load_sample_data()

# Page content based on navigation
if page == "Overview":
    st.header("League Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Teams", teams_count)
    with col2:
        st.metric("Season Week", 13)
    with col3:
        st.metric("Avg Points/Team", f"{teams_df['Points For'].mean():.1f}")
    with col4:
        st.metric("Highest Scorer", teams_df.loc[teams_df['Points For'].idxmax(), 'Team'])
    
    # League standings
    st.subheader("Current Standings")
    standings = teams_df.copy()
    standings['Win %'] = standings['Wins'] / (standings['Wins'] + standings['Losses'])
    standings = standings.sort_values(['Wins', 'Points For'], ascending=[False, False])
    standings.reset_index(drop=True, inplace=True)
    standings.index += 1
    st.dataframe(standings[['Team', 'Owner', 'Wins', 'Losses', 'Win %', 'Points For', 'Points Against']], width='stretch')
    
    # Points distribution chart
    st.subheader("Points Distribution")
    fig = px.bar(standings, x='Team', y='Points For', title='Total Points by Team')
    st.plotly_chart(fig, width='stretch')

elif page == "Team Analysis":
    st.header("Team Analysis")
    
    selected_team = st.selectbox("Select Team", teams_df['Team'].tolist())
    team_data = teams_df[teams_df['Team'] == selected_team].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Wins", int(team_data['Wins']))
        st.metric("Points For", f"{team_data['Points For']:.1f}")
    with col2:
        st.metric("Losses", int(team_data['Losses']))
        st.metric("Points Against", f"{team_data['Points Against']:.1f}")
    
    # Performance chart
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Points For', x=['Selected Team'], y=[team_data['Points For']]))
    fig.add_trace(go.Bar(name='League Average', x=['Selected Team'], y=[teams_df['Points For'].mean()]))
    fig.update_layout(title=f"{selected_team} vs League Average")
    st.plotly_chart(fig, width='stretch')

elif page == "Player Stats":
    st.header("Player Statistics")
    
    st.subheader("Top Performers")
    st.dataframe(players_df, width='stretch')
    
    # Player performance chart
    fig = px.scatter(players_df, x='Games', y='Points', color='Position', 
                    hover_data=['Player', 'Team'], title='Player Performance')
    st.plotly_chart(fig, width='stretch')

elif page == "Matchup Predictor":
    st.header("Matchup Predictor")
    
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Team 1", teams_df['Team'].tolist(), key="team1")
    with col2:
        team2 = st.selectbox("Team 2", teams_df['Team'].tolist(), key="team2")
    
    if team1 != team2:
        team1_data = teams_df[teams_df['Team'] == team1].iloc[0]
        team2_data = teams_df[teams_df['Team'] == team2].iloc[0]
        
        st.subheader("Matchup Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{team1}**")
            st.write(f"Record: {int(team1_data['Wins'])}-{int(team1_data['Losses'])}")
            st.write(f"Avg Points: {team1_data['Points For']/(team1_data['Wins']+team1_data['Losses']):.1f}")
        
        with col2:
            st.write(f"**{team2}**")
            st.write(f"Record: {int(team2_data['Wins'])}-{int(team2_data['Losses'])}")
            st.write(f"Avg Points: {team2_data['Points For']/(team2_data['Wins']+team2_data['Losses']):.1f}")
        
        # Simple prediction based on average points
        team1_avg = team1_data['Points For']/(team1_data['Wins']+team1_data['Losses'])
        team2_avg = team2_data['Points For']/(team2_data['Wins']+team2_data['Losses'])
        
        if team1_avg > team2_avg:
            st.success(f"Prediction: {team1} favored to win")
        else:
            st.success(f"Prediction: {team2} favored to win")

elif page == "Waiver Wire":
    st.header("Waiver Wire Analysis")
    
    st.info("Waiver wire recommendations coming soon!")
    st.write("This section will include:")
    st.write("- Available players analysis")
    st.write("- Pickup recommendations") 
    st.write("- Drop candidates")
    st.write("- Injury replacements")

# Footer
st.markdown("---")
st.markdown("*Fantasy Football 2025 Dashboard - Built with Streamlit*")