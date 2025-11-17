#!/usr/bin/env python3
"""
FantasyAI Pro - AI-Powered Fantasy Football Analysis Suite

Advanced fantasy football analysis tool combining trending data, performance analytics,
and visual charts to optimize your roster decisions.

Features:
- Quick scan mode: Fast check of trending players
- Full analysis mode: Detailed roster analysis with swap suggestions
- Performance analysis: Track actual fantasy points to identify underperformers
- Chart mode: Visual weekly performance charts for your roster
- Real-time data integration with Sleeper API
- AI-powered recommendations for optimal roster management

Usage:
    python fantasyai_pro.py                 # Quick scan (default)
    python fantasyai_pro.py quick           # Quick scan
    python fantasyai_pro.py full            # Full analysis
    python fantasyai_pro.py performance     # Performance analysis
    python fantasyai_pro.py chart           # Performance with visual chart
    python fantasyai_pro.py demo            # Demo chart with sample data
    python fantasyai_pro.py help            # Show help

Author: GitHub Gridiron Team (AI-Assisted Fantasy Analysis)
"""

import requests
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict

# Configuration - Update these for your league
SLEEPER_API_BASE = "https://api.sleeper.app/v1"
USERNAME = "ryanmcpeck"  # Your Sleeper username
SEASON = "2025"          # Current NFL season

# Performance tracking settings
WEEKS_TO_ANALYZE = 3     # Number of recent weeks to analyze for performance
POOR_PERFORMANCE_THRESHOLD = 8.0  # Fantasy points below this = poor performance

# Rate limiting protection (Sleeper allows 1000 calls/minute)
API_CALL_DELAY = 0.1  # Small delay between API calls (100ms)

def safe_api_call(url, params=None):
    """
    Make a rate-limited API call to prevent hitting Sleeper's 1000 calls/minute limit.
    
    Args:
        url (str): API endpoint URL
        params (dict): Optional query parameters
        
    Returns:
        dict: JSON response from API
    """
    time.sleep(API_CALL_DELAY)  # Small delay to respect rate limits
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

def get_user_id(username):
    """
    Get Sleeper user ID from username.
    
    Args:
        username (str): Your Sleeper username
        
    Returns:
        str: Your unique Sleeper user ID
    """
    url = f"{SLEEPER_API_BASE}/user/{username}"
    return safe_api_call(url)["user_id"]

def get_leagues(user_id, season):
    """
    Get all leagues for a user in a given season.
    
    Args:
        user_id (str): Sleeper user ID
        season (str): NFL season year
        
    Returns:
        list: List of league dictionaries containing league info
    """
    url = f"{SLEEPER_API_BASE}/user/{user_id}/leagues/nfl/{season}"
    return safe_api_call(url)

def get_nfl_players():
    """
    Get comprehensive NFL player database from Sleeper.
    This includes all active and inactive players with stats, positions, teams, etc.
    
    Returns:
        dict: Dictionary where keys are player IDs and values are player info
    """
    url = f"{SLEEPER_API_BASE}/players/nfl"
    return safe_api_call(url)

def get_trending_players(sport="nfl", add_drop="add", hours=24, limit=25):
    """
    Get players that are trending on waiver wires (being added/dropped frequently).
    This is key data - shows which players other fantasy managers are targeting.
    
    Args:
        sport (str): Sport type (default: "nfl")
        add_drop (str): "add" for pickups, "drop" for drops (default: "add")
        hours (int): Lookback period in hours (default: 24)
        limit (int): Max number of players to return (default: 25)
        
    Returns:
        list: List of trending player data with add/drop counts
    """
    url = f"{SLEEPER_API_BASE}/players/{sport}/trending/{add_drop}"
    params = {"lookback_hours": hours, "limit": limit}
    return safe_api_call(url, params)

def get_trending_drops(hours=24, limit=25):
    """
    Get players that are being dropped frequently (trending downward).
    Useful for identifying players to consider cutting from your roster.
    
    Args:
        hours (int): Lookback period in hours (default: 24)
        limit (int): Max number of players to return (default: 25)
        
    Returns:
        list: List of players being dropped frequently
    """
    return get_trending_players(add_drop="drop", hours=hours, limit=limit)

def get_league_stats(league_id, week):
    """
    Get fantasy stats for all players in a specific week.
    This shows actual fantasy points scored, not just trending data.
    
    Args:
        league_id (str): Your league ID
        week (int): NFL week number
        
    Returns:
        dict: Player stats for the specified week
    """
    # Use the correct NFL stats endpoint instead of league-specific
    url = f"{SLEEPER_API_BASE}/stats/nfl/regular/{SEASON}/{week}"
    try:
        return safe_api_call(url)
    except:
        # Return empty dict if stats not available for that week
        return {}

def get_current_nfl_week():
    """
    Get the current NFL week number.
    
    Returns:
        int: Current NFL week (1-18)
    """
    # For 2025 season, estimate based on date
    # NFL season typically starts first Thursday of September
    # For testing purposes, return a week that has data
    return 10  # Mid-November would be around week 10-11

def analyze_player_performance(player_ids, league_id, all_players, weeks_back=3):
    """
    Analyze recent performance of your roster players to identify underperformers.
    This looks at actual fantasy points scored, not just trending data.
    
    Args:
        player_ids (list): List of player IDs to analyze
        league_id (str): Your league ID
        all_players (dict): Complete NFL player database
        weeks_back (int): Number of recent weeks to analyze
        
    Returns:
        list: Players with poor recent performance
    """
    current_week = get_current_nfl_week()
    poor_performers = []
    
    print(f"  Analyzing weeks {max(1, current_week - weeks_back + 1)} through {current_week}...")
    
    # Analyze performance over recent weeks
    for week in range(max(1, current_week - weeks_back + 1), current_week + 1):
        week_stats = get_league_stats(league_id, week)
        
        if not week_stats:
            print(f"  No stats data available for week {week}")
            continue
            
        print(f"  Processing week {week} stats ({len(week_stats)} players)...")
        
        # Check each of your players' performance
        for player_id in player_ids:
            if player_id in week_stats and player_id in all_players:
                player_info = all_players[player_id]
                stats = week_stats[player_id]
                
                # Get fantasy points (pts_ppr for PPR leagues, pts_std for standard)
                fantasy_points = stats.get('pts_ppr', stats.get('pts_std', stats.get('pts_half_ppr', 0)))
                
                # If player scored below threshold, add to poor performers
                if fantasy_points < POOR_PERFORMANCE_THRESHOLD:
                    name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip()
                    
                    # Check if already in list, if not add them
                    existing = next((p for p in poor_performers if p['player_id'] == player_id), None)
                    if existing:
                        existing['poor_weeks'].append({
                            'week': week,
                            'points': fantasy_points
                        })
                        existing['total_poor_weeks'] += 1
                    else:
                        poor_performers.append({
                            'player_id': player_id,
                            'name': name,
                            'position': player_info.get('position', 'N/A'),
                            'team': player_info.get('team', 'N/A'),
                            'poor_weeks': [{
                                'week': week,
                                'points': fantasy_points
                            }],
                            'total_poor_weeks': 1
                        })
    
    # Sort by number of poor weeks (most concerning first)
    poor_performers.sort(key=lambda x: x['total_poor_weeks'], reverse=True)
    
    return poor_performers

def find_available_players(league_id, rosters, all_players, trending_adds):
    """
    Cross-reference trending players with your league's rosters to find
    which hot pickups are actually available in YOUR league.
    
    Args:
        league_id (str): Your league ID
        rosters (list): All rosters in your league
        all_players (dict): Complete NFL player database
        trending_adds (list): Players trending upward on waivers
        
    Returns:
        list: Available players sorted by trending popularity
    """
    # Step 1: Get all players already on rosters in your league
    rostered_player_ids = set()
    for roster in rosters:
        if roster.get('players'):  # Some rosters might be empty
            rostered_player_ids.update(roster['players'])
    
    # Step 2: Filter trending players to only those available in your league
    available_trending = []
    for player_data in trending_adds:
        player_id = player_data['player_id']
        
        # Check if player is available (not rostered) and exists in NFL database
        if player_id not in rostered_player_ids and player_id in all_players:
            player_info = all_players[player_id]
            
            # Only include active NFL players
            if player_info and player_info.get('active', False):
                available_trending.append({
                    'player_id': player_id,
                    'name': f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip(),
                    'position': player_info.get('position', 'N/A'),
                    'team': player_info.get('team', 'N/A'),
                    'trend_count': player_data.get('count', 0)  # How many times added
                })
    
    return available_trending

def check_your_players_trending_down(your_roster_players, all_players, trending_drops):
    """
    Check if any of your rostered players are trending downward (being dropped).
    This helps identify players you might want to cut before they lose more value.
    
    Args:
        your_roster_players (list): Your current roster player IDs
        all_players (dict): Complete NFL player database
        trending_drops (list): Players being dropped frequently
        
    Returns:
        list: Your players that are trending downward
    """
    your_players_dropping = []
    
    # Get trending drop player IDs for easy lookup
    trending_drop_ids = {player_data['player_id'] for player_data in trending_drops}
    
    # Check if any of your players are in the trending drops list
    for player_id in your_roster_players:
        if player_id in trending_drop_ids and player_id in all_players:
            # Find the drop data for this player
            drop_data = next((p for p in trending_drops if p['player_id'] == player_id), None)
            if drop_data:
                player_info = all_players[player_id]
                name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip()
                your_players_dropping.append({
                    'player_id': player_id,
                    'name': name,
                    'position': player_info.get('position', 'N/A'),
                    'team': player_info.get('team', 'N/A'),
                    'drop_count': drop_data.get('count', 0)
                })
    
    return your_players_dropping

def analyze_roster_vs_available(your_roster_players, available_players, all_players):
    """
    Compare your current roster to available trending players and suggest swaps.
    This function provides position-specific recommendations for roster moves.
    
    Args:
        your_roster_players (list): Your current roster player IDs
        available_players (list): Available trending players
        all_players (dict): Complete NFL player database
    """
    print("\n🔄 SWAP RECOMMENDATIONS:")
    print("=" * 60)
    
    # Step 1: Build your current roster data
    your_bench = []
    for player_id in your_roster_players:
        if player_id in all_players:
            player_info = all_players[player_id]
            name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip()
            position = player_info.get('position', 'N/A')
            team = player_info.get('team', 'N/A')
            your_bench.append({
                'name': name, 'position': position, 'team': team, 'player_id': player_id
            })
    
    # Step 2: Group available players by position for easier comparison
    available_by_pos = {}
    for player in available_players[:15]:  # Focus on top 15 trending
        pos = player['position']
        if pos not in available_by_pos:
            available_by_pos[pos] = []
        available_by_pos[pos].append(player)
    
    # Step 3: Show position-by-position swap suggestions
    for pos, available_list in available_by_pos.items():
        if available_list:
            print(f"\n{pos} Options:")
            for player in available_list[:3]:  # Top 3 per position
                print(f"  ⬆️  {player['name']} ({player['team']}) - {player['trend_count']:,} adds")
            
            # Show your current players at this position for comparison
            your_pos_players = [p for p in your_bench if p['position'] == pos]
            if your_pos_players:
                print(f"  Your {pos}s: {', '.join([p['name'] for p in your_pos_players[:2]])}")

def quick_scan_mode():
    """
    Fast waiver wire scan - perfect for daily checks.
    Shows only the top 5 trending pickups available in your league.
    
    This mode is optimized for speed and regular use. Run it every morning
    or after games to catch breakout performances early.
    """
    print(f"\n⚡ QUICK SCAN - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # Step 1: Get your league information
    user_id = get_user_id(USERNAME)
    leagues = get_leagues(user_id, SEASON)
    league = leagues[0]  # Use first league (modify if you're in multiple)
    league_id = league['league_id']
    
    # Step 2: Get all rosters to see who's available
    rosters_url = f"{SLEEPER_API_BASE}/league/{league_id}/rosters"
    rosters = safe_api_call(rosters_url)
    
    # Step 3: Find your specific roster
    your_roster = None
    for roster in rosters:
        if roster.get('owner_id') == user_id:
            your_roster = roster
            break
    
    # Step 4: Get trending data (limited set for speed)
    print("Fetching trending players...")
    trending_adds = get_trending_players(limit=10)  # Only top 10 for speed
    trending_drops = get_trending_drops(limit=10)   # Check for your players being dropped
    all_players = get_nfl_players()
    
    # Step 5: Find which trending players are actually available
    available_players = find_available_players(league_id, rosters, all_players, trending_adds)
    
    # Step 6: Check if any of your players are trending down
    your_dropping_players = check_your_players_trending_down(
        your_roster['players'], all_players, trending_drops
    )
    
    # Step 7: Display results
    if available_players:
        print(f"\n🔥 HOT PICKUPS RIGHT NOW:")
        for i, player in enumerate(available_players[:5], 1):
            print(f"{i}. {player['name']} ({player['position']}) - {player['team']} - {player['trend_count']:,} adds")
    else:
        print("No trending players available on waivers right now.")
    
    # Step 8: Alert about your players being dropped
    if your_dropping_players:
        print(f"\n⚠️  YOUR PLAYERS BEING DROPPED:")
        for player in your_dropping_players:
            print(f"❌ {player['name']} ({player['position']}) - {player['team']} - {player['drop_count']:,} drops")
        print("Consider cutting these players before they lose more value!")
    else:
        print(f"\n✅ None of your players are trending downward.")

def collect_weekly_performance_data(player_ids, league_id, all_players, weeks_back=6):
    """
    Collect comprehensive weekly performance data for charting.
    Returns detailed week-by-week performance for each player.
    
    Args:
        player_ids (list): List of player IDs to analyze
        league_id (str): Your league ID
        all_players (dict): Complete NFL player database
        weeks_back (int): Number of weeks to collect data for
        
    Returns:
        dict: Player performance data organized by player
    """
    current_week = get_current_nfl_week()
    player_performance = defaultdict(lambda: {'name': '', 'position': '', 'team': '', 'weeks': []})
    
    print(f"  Collecting chart data for weeks {max(1, current_week - weeks_back + 1)} through {current_week}...")
    
    # Collect data for each week
    for week in range(max(1, current_week - weeks_back + 1), current_week + 1):
        week_stats = get_league_stats(league_id, week)
        
        if not week_stats:
            print(f"  No data for week {week}")
            continue
            
        # Record performance for each player
        for player_id in player_ids:
            if player_id in all_players:
                player_info = all_players[player_id]
                
                # Initialize player info if first time seeing them
                if not player_performance[player_id]['name']:
                    name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip()
                    player_performance[player_id]['name'] = name
                    player_performance[player_id]['position'] = player_info.get('position', 'N/A')
                    player_performance[player_id]['team'] = player_info.get('team', 'N/A')
                
                # Get fantasy points for this week
                points = 0
                if player_id in week_stats:
                    stats = week_stats[player_id]
                    points = stats.get('pts_ppr', stats.get('pts_std', stats.get('pts_half_ppr', 0)))
                
                player_performance[player_id]['weeks'].append({
                    'week': week,
                    'points': points
                })
    
    return dict(player_performance)

def create_demo_performance_chart():
    """
    Create a demo performance chart with sample data to show charting capabilities.
    This is useful when actual stats data is not available.
    """
    print("\n📊 Creating demo performance chart with sample data...")
    
    # Sample data based on your actual roster
    demo_data = {
        'player_1': {
            'name': 'Brock Purdy',
            'position': 'QB',
            'team': 'SF',
            'weeks': [
                {'week': 9, 'points': 24.2},
                {'week': 10, 'points': 18.6},
                {'week': 11, 'points': 22.1}
            ]
        },
        'player_2': {
            'name': 'Breece Hall',
            'position': 'RB',
            'team': 'NYJ',
            'weeks': [
                {'week': 9, 'points': 15.4},
                {'week': 10, 'points': 11.8},
                {'week': 11, 'points': 19.3}
            ]
        },
        'player_3': {
            'name': 'Garrett Wilson',
            'position': 'WR',
            'team': 'NYJ',
            'weeks': [
                {'week': 9, 'points': 12.7},
                {'week': 10, 'points': 8.9},
                {'week': 11, 'points': 16.2}
            ]
        },
        'player_4': {
            'name': 'Jerry Jeudy',
            'position': 'WR',
            'team': 'CLE',
            'weeks': [
                {'week': 9, 'points': 4.2},
                {'week': 10, 'points': 2.1},
                {'week': 11, 'points': 5.8}
            ]
        },
        'player_5': {
            'name': 'Terry McLaurin',
            'position': 'WR',
            'team': 'WAS',
            'weeks': [
                {'week': 9, 'points': 18.4},
                {'week': 10, 'points': 14.7},
                {'week': 11, 'points': 21.3}
            ]
        },
        'player_6': {
            'name': 'D\'Andre Swift',
            'position': 'RB',
            'team': 'CHI',
            'weeks': [
                {'week': 9, 'points': 13.2},
                {'week': 10, 'points': 9.4},
                {'week': 11, 'points': 16.7}
            ]
        }
    }
    
    create_performance_chart(demo_data, weeks_back=3)

def create_performance_chart(player_data, weeks_back=6):
    """
    Create a visual chart showing weekly performance for each player.
    
    Args:
        player_data (dict): Player performance data from collect_weekly_performance_data
        weeks_back (int): Number of weeks shown in chart
    """
    if not player_data:
        print("❌ No performance data available for charting.")
        return
    
    # Set up the plot
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Color map for different positions
    position_colors = {
        'QB': '#FF6B6B', 'RB': '#4ECDC4', 'WR': '#45B7D1', 
        'TE': '#96CEB4', 'K': '#FECA57', 'DEF': '#FF9FF3'
    }
    
    current_week = get_current_nfl_week()
    weeks = list(range(max(1, current_week - weeks_back + 1), current_week + 1))
    
    # Plot each player's performance
    for player_id, data in player_data.items():
        if not data['weeks']:  # Skip if no data
            continue
            
        player_name = data['name']
        position = data['position']
        team = data['team']
        
        # Extract weekly points in order
        weekly_points = []
        for week in weeks:
            week_data = next((w for w in data['weeks'] if w['week'] == week), None)
            points = week_data['points'] if week_data else 0
            weekly_points.append(points)
        
        # Get color for this position
        color = position_colors.get(position, '#95A5A6')
        
        # Plot the line
        ax.plot(weeks, weekly_points, 
                marker='o', linewidth=2.5, markersize=6,
                color=color, alpha=0.8,
                label=f"{player_name} ({position}) - {team}")
        
        # Add point labels for clarity
        for i, (week, points) in enumerate(zip(weeks, weekly_points)):
            if points > 0:  # Only label non-zero scores
                ax.annotate(f'{points:.1f}', 
                           (week, points), 
                           textcoords="offset points", 
                           xytext=(0,8), 
                           ha='center', 
                           fontsize=8, 
                           alpha=0.7)
    
    # Customize the chart
    ax.set_xlabel('NFL Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Fantasy Points', fontsize=12, fontweight='bold')
    ax.set_title('🏈 GitHub Gridiron - Weekly Performance Chart\n' + 
                f'Weeks {weeks[0]}-{weeks[-1]} Fantasy Points by Player', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Add threshold line for poor performance
    ax.axhline(y=8.0, color='red', linestyle='--', alpha=0.6, 
               label='Poor Performance Threshold (8.0 pts)')
    
    # Customize grid and layout
    ax.grid(True, alpha=0.3)
    ax.set_xticks(weeks)
    ax.set_xlim(weeks[0] - 0.2, weeks[-1] + 0.2)
    
    # Legend with position grouping
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(1.02, 1), 
              fontsize=9, framealpha=0.9)
    
    # Tight layout to prevent cutoff
    plt.tight_layout()
    
    # Save the chart
    chart_filename = f"charts/weekly_performance_chart_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    
    print(f"\n📊 Performance chart saved as: {chart_filename}")
    print("📈 Chart shows weekly fantasy points for each player over recent weeks")
    print("🔴 Red dashed line shows poor performance threshold (8.0 pts)")
    
    # Display the chart
    plt.show()

def performance_analysis_mode(show_chart=False):
    """
    Weekly performance analysis - identifies players performing poorly based on actual fantasy points.
    
    This mode provides:
    - Analysis of your players' recent fantasy point totals
    - Identification of consistent underperformers 
    - Performance trends over recent weeks
    - Recommendations for players to consider dropping based on poor output
    - Optional visual chart showing weekly performance trends
    
    Args:
        show_chart (bool): Whether to generate and display a performance chart
    
    Use this mode to identify roster dead weight and make performance-based decisions.
    """
    print(f"\n📈 PERFORMANCE ANALYSIS - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Step 1: Get league and roster data
    user_id = get_user_id(USERNAME)
    leagues = get_leagues(user_id, SEASON)
    league = leagues[0]
    league_id = league['league_id']
    
    rosters_url = f"{SLEEPER_API_BASE}/league/{league_id}/rosters"
    rosters = safe_api_call(rosters_url)
    
    your_roster = None
    for roster in rosters:
        if roster.get('owner_id') == user_id:
            your_roster = roster
            break
    
    if not your_roster or not your_roster.get('players'):
        print("❌ Could not find your roster!")
        return
    
    # Step 2: Load player data and analyze performance
    print("Loading player data and analyzing recent performance...")
    all_players = get_nfl_players()
    
    poor_performers = analyze_player_performance(
        your_roster['players'], league_id, all_players, WEEKS_TO_ANALYZE
    )
    
    # Step 3: Display performance analysis results
    current_week = get_current_nfl_week()
    print(f"\n📊 PERFORMANCE ANALYSIS - Last {WEEKS_TO_ANALYZE} Weeks (Weeks {current_week-WEEKS_TO_ANALYZE+1}-{current_week})")
    print("-" * 60)
    
    if poor_performers:
        print(f"⚠️  UNDERPERFORMING PLAYERS (< {POOR_PERFORMANCE_THRESHOLD} pts):")
        for player in poor_performers:
            weeks_text = f"{player['total_poor_weeks']}/{WEEKS_TO_ANALYZE} weeks"
            recent_points = [str(w['points']) for w in player['poor_weeks'][-2:]]  # Last 2 poor performances
            print(f"❌ {player['name']} ({player['position']}) - {player['team']} - {weeks_text} below threshold")
            print(f"   Recent poor weeks: {', '.join(recent_points)} pts")
        
        print(f"\n💡 RECOMMENDATION: Consider dropping players with 2+ poor weeks for trending adds!")
    else:
        print(f"✅ No players consistently underperforming (below {POOR_PERFORMANCE_THRESHOLD} pts)")
        print("Your roster is performing well from a points perspective!")
    
    # Step 4: Show top/bottom performers for context
    print(f"\n🏆 PERFORMANCE CONTEXT:")
    print("Consider combining this analysis with trending data for optimal decisions.")
    print("Players can have good underlying performance but still be droppable if better options emerge.")
    
    # Step 5: Generate chart if requested
    if show_chart:
        print(f"\n📊 Generating performance chart...")
        chart_data = collect_weekly_performance_data(
            your_roster['players'], league_id, all_players, weeks_back=6
        )
        
        if not chart_data or not any(data['weeks'] for data in chart_data.values()):
            print("⚠️  No recent performance data available from Sleeper API.")
            print("🎯 Creating demo chart to show visualization capabilities...")
            create_demo_performance_chart()
        else:
            create_performance_chart(chart_data, weeks_back=6)

def full_analysis_mode():
    """
    Comprehensive roster analysis with detailed swap recommendations.
    
    This mode provides:
    - Complete view of your roster organized by position
    - Top 25 trending players analysis
    - Specific position-based swap suggestions
    - Comparison between your current players and available options
    - Performance analysis integration
    
    Use this mode when you want to make strategic roster decisions,
    especially before waiver deadlines.
    """
    print(f"\n📊 FULL ANALYSIS - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Step 1: Get league and roster data
    user_id = get_user_id(USERNAME)
    leagues = get_leagues(user_id, SEASON)
    league = leagues[0]
    league_id = league['league_id']
    
    rosters_url = f"{SLEEPER_API_BASE}/league/{league_id}/rosters"
    rosters = safe_api_call(rosters_url)
    
    your_roster = None
    for roster in rosters:
        if roster.get('owner_id') == user_id:
            your_roster = roster
            break
    
    # Step 2: Load comprehensive player data
    print("Loading player data...")
    all_players = get_nfl_players()
    trending_adds = get_trending_players(limit=25)  # More detailed analysis
    trending_drops = get_trending_drops(limit=25)   # Check for players being dropped
    
    available_players = find_available_players(league_id, rosters, all_players, trending_adds)
    your_dropping_players = check_your_players_trending_down(
        your_roster['players'], all_players, trending_drops
    )
    
    # Step 3: Display your current roster organized by position
    if your_roster.get('players'):
        print(f"\n📋 YOUR ROSTER ({len(your_roster['players'])} players):")
        roster_by_pos = {}
        for player_id in your_roster['players']:
            if player_id in all_players:
                player_info = all_players[player_id]
                name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip()
                pos = player_info.get('position', 'N/A')
                team = player_info.get('team', 'N/A')
                
                # Mark players that are trending down
                is_dropping = any(p['player_id'] == player_id for p in your_dropping_players)
                display_name = f"{name} ({team})"
                if is_dropping:
                    display_name += " ⚠️"
                
                if pos not in roster_by_pos:
                    roster_by_pos[pos] = []
                roster_by_pos[pos].append(display_name)
        
        # Display roster by position for easy analysis
        for pos, players in roster_by_pos.items():
            print(f"{pos}: {', '.join(players)}")
    
    # Step 4: Show trending drop alerts
    if your_dropping_players:
        print(f"\n⚠️  ROSTER ALERTS - Players Being Dropped:")
        print("-" * 60)
        for player in your_dropping_players:
            print(f"❌ {player['name']} ({player['position']}) - {player['team']} - {player['drop_count']:,} drops")
        print("💡 Consider cutting these players for trending adds!")
    
    # Step 5: Quick performance check
    poor_performers = analyze_player_performance(
        your_roster['players'], league_id, all_players, 2  # Quick 2-week check
    )
    
    if poor_performers:
        print(f"\n📉 RECENT POOR PERFORMERS (< {POOR_PERFORMANCE_THRESHOLD} pts):")
        print("-" * 60)
        for player in poor_performers[:3]:  # Show top 3 poor performers
            print(f"⚠️  {player['name']} ({player['position']}) - {player['total_poor_weeks']}/2 recent poor weeks")
        print("💡 Run 'performance' mode for detailed analysis!")
    
    # Step 6: Provide detailed swap analysis
    if available_players:
        analyze_roster_vs_available(your_roster['players'], available_players, all_players)

def main():
    """
    Main function that handles command-line arguments and runs the appropriate analysis mode.
    
    The script supports multiple modes:
    - quick/q: Fast daily check (default)
    - full/f: Comprehensive analysis 
    - help/h: Show usage information
    """
    print("🤖 FantasyAI Pro - Advanced Fantasy Football Analysis")
    print("=" * 50)
    print("🏈 Powered by GitHub Gridiron AI")
    
    # Parse command line arguments (defaults to 'quick' if none provided)
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = "quick"  # Default mode for daily use
    
    # Route to appropriate analysis function
    try:
        if mode == "quick" or mode == "q":
            quick_scan_mode()
        elif mode == "full" or mode == "f":
            full_analysis_mode()
        elif mode == "performance" or mode == "p":
            performance_analysis_mode()
        elif mode == "chart" or mode == "c":
            performance_analysis_mode(show_chart=True)
        elif mode == "demo" or mode == "d":
            create_demo_performance_chart()
        elif mode == "gameplan" or mode == "g":
            generate_weekly_gameplan()
        elif mode == "help" or mode == "h":
            print_help()
        else:
            print(f"Unknown mode: {mode}")
            print_help()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Try running with 'help' argument for usage info.")

def print_help():
    """Display usage instructions and examples."""
    print("\n📖 FANTASYAI PRO - USAGE GUIDE")
    print("=" * 40)
    print("\n🔧 ANALYSIS MODES:")
    print("  quick, q       - Quick trending scan (daily use)")
    print("  full, f        - Complete roster analysis")
    print("  performance, p - Performance analytics (actual points)")
    print("  chart, c       - Visual performance charts")
    print("  demo, d        - Demo charts with sample data")
    print("  gameplan, g    - Weekly game plan generator")
    print("  help, h        - Show this help")
    
    print("\n💡 EXAMPLES:")
    print("  python fantasyai_pro.py                 # Quick scan")
    print("  python fantasyai_pro.py full            # Full analysis")
    print("  python fantasyai_pro.py performance     # Performance analysis")
    print("  python fantasyai_pro.py chart           # Visual charts")
    print("  python fantasyai_pro.py gameplan        # Weekly game plan")
    
    print("\n🎯 WEEKLY WORKFLOW:")
    print("  1. Daily: Run 'quick' to catch trending players")
    print("  2. Tuesday: Run 'performance' to identify underperformers")
    print("  3. Wednesday: Run 'full' before waiver deadlines")
    print("  4. Weekly: Generate 'chart' for visual analysis")
    
    print("\n📊 DATA INSIGHTS:")
    print("  • Trending counts = how many managers added each player")
    print("  • Performance threshold = 8.0 fantasy points")
    print("  • Charts show 6-week performance trends")
    print("  🔴 Red line indicates poor performance threshold")

def generate_weekly_gameplan():
    """
    Generate a comprehensive weekly game plan based on current analysis.
    This runs after games are complete to plan for the upcoming week.
    """
    print("\n📋 FANTASYAI PRO - WEEKLY GAME PLAN")
    print("=" * 50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("\n🎯 THIS WEEK'S STRATEGY:")
    
    # Step 1: Get comprehensive data
    user_id = get_user_id(USERNAME)
    leagues = get_leagues(user_id, SEASON)
    league = leagues[0]
    league_id = league['league_id']
    
    rosters_url = f"{SLEEPER_API_BASE}/league/{league_id}/rosters"
    rosters = safe_api_call(rosters_url)
    
    your_roster = None
    for roster in rosters:
        if roster.get('owner_id') == user_id:
            your_roster = roster
            break
    
    if not your_roster:
        print("❌ Could not find your roster!")
        return
    
    print("Loading comprehensive analysis...")
    all_players = get_nfl_players()
    trending_adds = get_trending_players(limit=25)
    trending_drops = get_trending_drops(limit=25)
    
    # Step 2: Performance Analysis
    poor_performers = analyze_player_performance(
        your_roster['players'], league_id, all_players, weeks_back=3
    )
    
    # Step 3: Available players analysis
    available_players = find_available_players(league_id, rosters, all_players, trending_adds)
    your_dropping_players = check_your_players_trending_down(
        your_roster['players'], all_players, trending_drops
    )
    
    # Step 4: Generate action plan
    print("\n🚨 IMMEDIATE ACTIONS (Priority Order):")
    print("-" * 40)
    
    action_count = 1
    
    # Priority 1: Drop consistent poor performers
    critical_drops = [p for p in poor_performers if p['total_poor_weeks'] >= 2]
    if critical_drops:
        print(f"{action_count}. 🗑️  DROP UNDERPERFORMERS:")
        for player in critical_drops[:3]:  # Top 3 priority drops
            print(f"   • {player['name']} ({player['position']}) - {player['total_poor_weeks']}/3 poor weeks")
        action_count += 1
    
    # Priority 2: Drop trending down players
    if your_dropping_players:
        print(f"{action_count}. 📉 DROP TRENDING DOWN:")
        for player in your_dropping_players[:2]:  # Top 2 trending drops
            print(f"   • {player['name']} ({player['position']}) - {player['drop_count']:,} drops")
        action_count += 1
    
    # Priority 3: Add hot trending players
    if available_players:
        print(f"{action_count}. 🔥 ADD HOT PICKUPS:")
        for player in available_players[:3]:  # Top 3 trending adds
            print(f"   • {player['name']} ({player['position']}) - {player['trend_count']:,} adds")
        action_count += 1
    
    # Step 5: Weekly schedule
    print("\n📅 THIS WEEK'S SCHEDULE:")
    print("-" * 40)
    print("🕘 Monday Night: Review game performances, run performance analysis")
    print("🕙 Tuesday: Execute priority drops, claim trending adds")
    print("🕚 Wednesday: Review waiver results, adjust lineup")
    print("🕛 Thursday: Monitor injury reports, make final adjustments")
    print("🕐 Weekend: Set optimal lineup, track player performance")
    
    # Step 6: Success metrics
    print("\n📊 SUCCESS METRICS:")
    print("-" * 40)
    roster_health = len([p for p in poor_performers if p['total_poor_weeks'] >= 2])
    if roster_health == 0:
        print("✅ Roster Health: EXCELLENT (No consistent underperformers)")
    elif roster_health <= 2:
        print(f"⚠️  Roster Health: GOOD ({roster_health} players need attention)")
    else:
        print(f"🚨 Roster Health: POOR ({roster_health} players underperforming)")
    
    trending_score = len([p for p in your_dropping_players if p['drop_count'] > 10000])
    if trending_score == 0:
        print("✅ Trending Score: EXCELLENT (No players being heavily dropped)")
    else:
        print(f"⚠️  Trending Score: {trending_score} players trending down")
    
    print("\n🏆 CHAMPIONSHIP FOCUS:")
    print("Continue using FantasyAI Pro's data-driven approach to stay ahead of your league!")

# Entry point - runs when script is executed directly

def generate_weekly_gameplan():
    """
    Generate a comprehensive weekly game plan based on current analysis.
    This runs after games are complete to plan for the upcoming week.
    """
    print("\n📋 FANTASYAI PRO - WEEKLY GAME PLAN")
    print("=" * 50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("\n🎯 THIS WEEK'S STRATEGY:")
    
    # Step 1: Get comprehensive data
    user_id = get_user_id(USERNAME)
    leagues = get_leagues(user_id, SEASON)
    league = leagues[0]
    league_id = league['league_id']
    
    rosters_url = f"{SLEEPER_API_BASE}/league/{league_id}/rosters"
    rosters = safe_api_call(rosters_url)
    
    your_roster = None
    for roster in rosters:
        if roster.get('owner_id') == user_id:
            your_roster = roster
            break
    
    if not your_roster:
        print("❌ Could not find your roster!")
        return
    
    print("Loading comprehensive analysis...")
    all_players = get_nfl_players()
    trending_adds = get_trending_players(limit=25)
    trending_drops = get_trending_drops(limit=25)
    
    # Step 2: Performance Analysis
    poor_performers = analyze_player_performance(
        your_roster['players'], league_id, all_players, weeks_back=3
    )
    
    # Step 3: Available players analysis
    available_players = find_available_players(league_id, rosters, all_players, trending_adds)
    your_dropping_players = check_your_players_trending_down(
        your_roster['players'], all_players, trending_drops
    )
    
    # Step 4: Generate action plan
    print("\n🚨 IMMEDIATE ACTIONS (Priority Order):")
    print("-" * 40)
    
    action_count = 1
    
    # Priority 1: Drop consistent poor performers
    critical_drops = [p for p in poor_performers if p['total_poor_weeks'] >= 2]
    if critical_drops:
        print(f"{action_count}. 🗑️  DROP UNDERPERFORMERS:")
        for player in critical_drops[:3]:  # Top 3 priority drops
            print(f"   • {player['name']} ({player['position']}) - {player['total_poor_weeks']}/3 poor weeks")
        action_count += 1
    
    # Priority 2: Drop trending down players
    if your_dropping_players:
        print(f"{action_count}. 📉 DROP TRENDING DOWN:")
        for player in your_dropping_players[:2]:  # Top 2 trending drops
            print(f"   • {player['name']} ({player['position']}) - {player['drop_count']:,} drops")
        action_count += 1
    
    # Priority 3: Add hot trending players
    if available_players:
        print(f"{action_count}. 🔥 ADD HOT PICKUPS:")
        for player in available_players[:3]:  # Top 3 trending adds
            print(f"   • {player['name']} ({player['position']}) - {player['trend_count']:,} adds")
        action_count += 1
    
    # Step 5: Weekly schedule
    print("\n📅 THIS WEEK'S SCHEDULE:")
    print("-" * 40)
    print("🕘 Monday Night: Review game performances, run performance analysis")
    print("🕙 Tuesday: Execute priority drops, claim trending adds")
    print("🕚 Wednesday: Review waiver results, adjust lineup")
    print("🕛 Thursday: Monitor injury reports, make final adjustments")
    print("🕐 Weekend: Set optimal lineup, track player performance")
    
    # Step 6: Success metrics
    print("\n📊 SUCCESS METRICS:")
    print("-" * 40)
    roster_health = len([p for p in poor_performers if p['total_poor_weeks'] >= 2])
    if roster_health == 0:
        print("✅ Roster Health: EXCELLENT (No consistent underperformers)")
    elif roster_health <= 2:
        print(f"⚠️  Roster Health: GOOD ({roster_health} players need attention)")
    else:
        print(f"🚨 Roster Health: POOR ({roster_health} players underperforming)")
    
    trending_score = len([p for p in your_dropping_players if p['drop_count'] > 10000])
    if trending_score == 0:
        print("✅ Trending Score: EXCELLENT (No players being heavily dropped)")
    else:
        print(f"⚠️  Trending Score: {trending_score} players trending down")
    
    print("\n🏆 CHAMPIONSHIP FOCUS:")
    print("Continue using FantasyAI Pro's data-driven approach to stay ahead of your league!")

# Entry point - runs when script is executed directly
if __name__ == "__main__":
    main()
