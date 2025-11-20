#!/usr/bin/env python3
"""
Trade Analyzer Module for FantasyAI Pro

This module provides trade analysis functionality to help evaluate potential trades
and identify optimal trade targets based on performance, trending data, and needs.

Usage:
    from trade_analyzer import analyze_trade, find_trade_targets
"""

import requests
from collections import defaultdict

def calculate_player_value(player_id, all_players, week_stats, trending_data):
    """
    Calculate a comprehensive fantasy value score for a player.
    
    Args:
        player_id (str): Sleeper player ID
        all_players (dict): Complete NFL player database
        week_stats (dict): Recent week statistics
        trending_data (dict): Trending add/drop information
        
    Returns:
        float: Player value score (higher = more valuable)
    """
    if player_id not in all_players:
        return 0
    
    player_info = all_players[player_id]
    position = player_info.get('position', '')
    
    # Base value by position (positional scarcity)
    position_values = {
        'QB': 1.0, 'RB': 1.5, 'WR': 1.3, 'TE': 1.2, 'K': 0.3, 'DEF': 0.4
    }
    base_value = position_values.get(position, 1.0)
    
    # Recent performance value (last few weeks)
    performance_value = 0
    if player_id in week_stats:
        stats = week_stats[player_id]
        recent_points = stats.get('pts_ppr', stats.get('pts_std', stats.get('pts_half_ppr', 0)))
        performance_value = recent_points / 20.0  # Normalize to 0-1 scale
    
    # Trending value (how much others want this player)
    trending_value = 0
    if trending_data:
        add_count = trending_data.get('adds', {}).get(player_id, 0)
        drop_count = trending_data.get('drops', {}).get(player_id, 0)
        net_trending = (add_count - drop_count) / 1000000.0  # Normalize
        trending_value = max(0, net_trending)  # Only positive trending counts
    
    # Age factor (younger players generally more valuable)
    age = player_info.get('age', 27)
    age_factor = max(0, (32 - age) / 10.0)  # Peak around 22-27
    
    # Injury penalty
    injury_penalty = 0
    injury_status = player_info.get('injury_status', '')
    if injury_status and injury_status.lower() in ['out', 'ir', 'suspended']:
        injury_penalty = 0.5
    elif injury_status and injury_status.lower() in ['doubtful', 'questionable']:
        injury_penalty = 0.2
    
    total_value = (base_value + performance_value + trending_value + age_factor) * (1 - injury_penalty)
    return max(0, total_value)

def analyze_trade(your_players, their_players, all_players, week_stats, trending_data):
    """
    Analyze a potential trade between you and another manager.
    
    Args:
        your_players (list): Player IDs you would trade away
        their_players (list): Player IDs you would receive
        all_players (dict): Complete NFL player database
        week_stats (dict): Recent week statistics
        trending_data (dict): Trending information
        
    Returns:
        dict: Trade analysis results
    """
    your_value = sum(calculate_player_value(pid, all_players, week_stats, trending_data) for pid in your_players)
    their_value = sum(calculate_player_value(pid, all_players, week_stats, trending_data) for pid in their_players)
    
    # Calculate value difference
    value_diff = their_value - your_value
    
    # Determine trade recommendation
    if value_diff > 0.5:
        recommendation = "ACCEPT - Great value!"
        trade_grade = "A"
    elif value_diff > 0.2:
        recommendation = "ACCEPT - Good trade"
        trade_grade = "B+"
    elif value_diff > -0.2:
        recommendation = "NEUTRAL - Fair trade"
        trade_grade = "B"
    elif value_diff > -0.5:
        recommendation = "DECLINE - Slightly unfavorable"
        trade_grade = "C"
    else:
        recommendation = "DECLINE - Bad trade for you"
        trade_grade = "D"
    
    # Get player details
    your_player_details = []
    for pid in your_players:
        if pid in all_players:
            p = all_players[pid]
            name = f"{p.get('first_name', '')} {p.get('last_name', '')}".strip()
            your_player_details.append(f"{name} ({p.get('position', 'N/A')})")
    
    their_player_details = []
    for pid in their_players:
        if pid in all_players:
            p = all_players[pid]
            name = f"{p.get('first_name', '')} {p.get('last_name', '')}".strip()
            their_player_details.append(f"{name} ({p.get('position', 'N/A')})")
    
    return {
        'recommendation': recommendation,
        'grade': trade_grade,
        'value_difference': value_diff,
        'your_value': your_value,
        'their_value': their_value,
        'your_players': your_player_details,
        'their_players': their_player_details
    }

def find_trade_targets(your_roster, league_rosters, all_players, week_stats, trending_data, position_need=None):
    """
    Identify potential trade targets based on your needs and other teams' rosters.
    
    Args:
        your_roster (list): Your current roster player IDs
        league_rosters (list): All rosters in your league
        all_players (dict): Complete NFL player database
        week_stats (dict): Recent performance data
        trending_data (dict): Trending information
        position_need (str): Specific position you're targeting (optional)
        
    Returns:
        list: Potential trade targets sorted by value
    """
    trade_targets = []
    
    # Calculate value of your players to identify trade assets
    your_player_values = {}
    for player_id in your_roster:
        your_player_values[player_id] = calculate_player_value(player_id, all_players, week_stats, trending_data)
    
    # Find valuable players on other teams
    for roster in league_rosters:
        if not roster.get('players') or roster.get('owner_id') in [your_roster]:
            continue
            
        for player_id in roster['players']:
            if player_id in all_players:
                player_info = all_players[player_id]
                position = player_info.get('position', '')
                
                # Skip if looking for specific position and this isn't it
                if position_need and position != position_need:
                    continue
                
                player_value = calculate_player_value(player_id, all_players, week_stats, trending_data)
                
                # Only consider players above a certain value threshold
                if player_value > 1.0:
                    name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip()
                    
                    trade_targets.append({
                        'player_id': player_id,
                        'name': name,
                        'position': position,
                        'team': player_info.get('team', 'N/A'),
                        'value': player_value,
                        'owner_id': roster.get('owner_id')
                    })
    
    # Sort by value (highest first)
    trade_targets.sort(key=lambda x: x['value'], reverse=True)
    
    return trade_targets[:20]  # Top 20 targets

def suggest_trade_packages(target_player, your_roster, all_players, week_stats, trending_data):
    """
    Suggest fair trade packages for a specific target player.
    
    Args:
        target_player (dict): Target player info from find_trade_targets
        your_roster (list): Your roster player IDs
        all_players (dict): Complete NFL player database
        week_stats (dict): Recent performance data
        trending_data (dict): Trending information
        
    Returns:
        list: Suggested trade packages
    """
    target_value = target_player['value']
    packages = []
    
    # Calculate your player values
    your_players = []
    for player_id in your_roster:
        if player_id in all_players:
            value = calculate_player_value(player_id, all_players, week_stats, trending_data)
            player_info = all_players[player_id]
            name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip()
            
            your_players.append({
                'player_id': player_id,
                'name': name,
                'position': player_info.get('position', ''),
                'value': value
            })
    
    # Sort by value
    your_players.sort(key=lambda x: x['value'], reverse=True)
    
    # Try single player trades first
    for player in your_players:
        value_ratio = player['value'] / target_value
        if 0.8 <= value_ratio <= 1.2:  # Fair trade range
            packages.append({
                'your_players': [player],
                'fairness': 'Fair',
                'total_value': player['value']
            })
    
    # Try two-player packages
    for i, player1 in enumerate(your_players):
        for player2 in your_players[i+1:]:
            combined_value = player1['value'] + player2['value']
            value_ratio = combined_value / target_value
            
            if 0.8 <= value_ratio <= 1.2:
                fairness = 'Fair' if 0.9 <= value_ratio <= 1.1 else 'Acceptable'
                packages.append({
                    'your_players': [player1, player2],
                    'fairness': fairness,
                    'total_value': combined_value
                })
    
    # Sort by fairness and value
    packages.sort(key=lambda x: (x['fairness'] == 'Fair', abs(x['total_value'] - target_value)))
    
    return packages[:5]  # Top 5 packages

def print_trade_analysis(trade_result):
    """
    Print formatted trade analysis results.
    
    Args:
        trade_result (dict): Results from analyze_trade function
    """
    print(f"\n🔄 TRADE ANALYSIS")
    print("=" * 50)
    
    print(f"📤 You give: {', '.join(trade_result['your_players'])}")
    print(f"📥 You get: {', '.join(trade_result['their_players'])}")
    
    print(f"\n📊 VALUE ASSESSMENT:")
    print(f"Your players value: {trade_result['your_value']:.2f}")
    print(f"Their players value: {trade_result['their_value']:.2f}")
    print(f"Value difference: {trade_result['value_difference']:+.2f}")
    
    print(f"\n💡 RECOMMENDATION: {trade_result['recommendation']}")
    print(f"📝 Trade Grade: {trade_result['grade']}")

def print_trade_targets(targets, position_filter=None):
    """
    Print formatted trade targets list.
    
    Args:
        targets (list): Results from find_trade_targets
        position_filter (str): Position to filter by (optional)
    """
    print(f"\n🎯 TRADE TARGETS")
    if position_filter:
        print(f"Position: {position_filter}")
    print("=" * 50)
    
    if not targets:
        print("No suitable trade targets found.")
        return
    
    for i, target in enumerate(targets[:10], 1):
        print(f"{i:2d}. {target['name']} ({target['position']}) - {target['team']}")
        print(f"    Value: {target['value']:.2f}")