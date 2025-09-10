#!/usr/bin/env python3
"""
Fantasy Waiver Wire Assistant - GitHub Gridiron Edition

This script helps you analyze your Sleeper fantasy football league to find
optimal waiver wire pickups and suggest roster improvements.

Features:
- Quick scan mode: Fast check of trending players
- Full analysis mode: Detailed roster analysis with swap suggestions
- Uses Sleeper API to get real-time data on trending player additions

Usage:
    python fantasy_waiver_assistant.py          # Quick scan (default)
    python fantasy_waiver_assistant.py quick    # Quick scan
    python fantasy_waiver_assistant.py full     # Full analysis
    python fantasy_waiver_assistant.py help     # Show help

Author: GitHub Gridiron (AI-Assisted Fantasy Team)
"""

import requests
import sys
from datetime import datetime

# Configuration - Update these for your league
SLEEPER_API_BASE = "https://api.sleeper.app/v1"
USERNAME = "ryanmcpeck"  # Your Sleeper username
SEASON = "2025"          # Current NFL season

def get_user_id(username):
    """
    Get Sleeper user ID from username.
    
    Args:
        username (str): Your Sleeper username
        
    Returns:
        str: Your unique Sleeper user ID
    """
    url = f"{SLEEPER_API_BASE}/user/{username}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["user_id"]

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
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_nfl_players():
    """
    Get comprehensive NFL player database from Sleeper.
    This includes all active and inactive players with stats, positions, teams, etc.
    
    Returns:
        dict: Dictionary where keys are player IDs and values are player info
    """
    url = f"{SLEEPER_API_BASE}/players/nfl"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

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
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

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
    rosters = requests.get(rosters_url).json()
    
    # Step 3: Find your specific roster
    your_roster = None
    for roster in rosters:
        if roster.get('owner_id') == user_id:
            your_roster = roster
            break
    
    # Step 4: Get trending data (limited set for speed)
    print("Fetching trending players...")
    trending_adds = get_trending_players(limit=10)  # Only top 10 for speed
    all_players = get_nfl_players()
    
    # Step 5: Find which trending players are actually available
    available_players = find_available_players(league_id, rosters, all_players, trending_adds)
    
    # Step 6: Display results
    if available_players:
        print(f"\n🔥 HOT PICKUPS RIGHT NOW:")
        for i, player in enumerate(available_players[:5], 1):
            print(f"{i}. {player['name']} ({player['position']}) - {player['team']} - {player['trend_count']:,} adds")
    else:
        print("No trending players available on waivers right now.")

def full_analysis_mode():
    """
    Comprehensive roster analysis with detailed swap recommendations.
    
    This mode provides:
    - Complete view of your roster organized by position
    - Top 25 trending players analysis
    - Specific position-based swap suggestions
    - Comparison between your current players and available options
    
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
    rosters = requests.get(rosters_url).json()
    
    your_roster = None
    for roster in rosters:
        if roster.get('owner_id') == user_id:
            your_roster = roster
            break
    
    # Step 2: Load comprehensive player data
    print("Loading player data...")
    all_players = get_nfl_players()
    trending_adds = get_trending_players(limit=25)  # More detailed analysis
    
    available_players = find_available_players(league_id, rosters, all_players, trending_adds)
    
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
                
                if pos not in roster_by_pos:
                    roster_by_pos[pos] = []
                roster_by_pos[pos].append(f"{name} ({team})")
        
        # Display roster by position for easy analysis
        for pos, players in roster_by_pos.items():
            print(f"{pos}: {', '.join(players)}")
    
    # Step 4: Provide detailed swap analysis
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
    print("🏈 GitHub Gridiron - AI Fantasy Assistant")
    print("=" * 40)
    
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
    print("\n📖 USAGE:")
    print("  python fantasy_waiver_assistant.py [mode]")
    print("\n🔧 MODES:")
    print("  quick, q    - Quick scan for hot pickups (default)")
    print("  full, f     - Full roster analysis with swap suggestions")
    print("  help, h     - Show this help message")
    print("\n💡 EXAMPLES:")
    print("  python fantasy_waiver_assistant.py           # Quick scan")
    print("  python fantasy_waiver_assistant.py quick     # Quick scan")
    print("  python fantasy_waiver_assistant.py full      # Full analysis")
    print("\n🎯 TIPS:")
    print("  - Run 'quick' daily to catch trending players early")
    print("  - Run 'full' before waiver deadlines for strategic decisions")
    print("  - Trending counts show how many managers added each player")

# Entry point - runs when script is executed directly
if __name__ == "__main__":
    main()
