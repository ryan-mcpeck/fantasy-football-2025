#!/usr/bin/env python3
"""
Injury Tracker Module for FantasyAI Pro

This module provides injury tracking functionality to enhance fantasy decision making.
Integrates with your existing FantasyAI Pro analyzer to provide injury context for roster moves.

Usage:
    from injury_tracker import get_injury_status, analyze_injury_impact
"""

import requests
import json
from datetime import datetime

SLEEPER_API_BASE = "https://api.sleeper.app/v1"

def get_injury_status(player_ids, all_players):
    """
    Get current injury status for specified players.
    
    Args:
        player_ids (list): List of Sleeper player IDs
        all_players (dict): Complete NFL player database from Sleeper
        
    Returns:
        list: Players with injury information
    """
    injured_players = []
    
    for player_id in player_ids:
        if player_id in all_players:
            player_info = all_players[player_id]
            
            # Check for injury status in player data
            injury_status = player_info.get('injury_status', None)
            injury_notes = player_info.get('injury_notes', '')
            injury_body_part = player_info.get('injury_body_part', '')
            
            if injury_status and injury_status.lower() != 'healthy':
                name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip()
                injured_players.append({
                    'player_id': player_id,
                    'name': name,
                    'position': player_info.get('position', 'N/A'),
                    'team': player_info.get('team', 'N/A'),
                    'injury_status': injury_status,
                    'injury_notes': injury_notes,
                    'injury_body_part': injury_body_part
                })
    
    return injured_players

def analyze_injury_impact(injured_players):
    """
    Analyze the fantasy impact of injuries.
    
    Args:
        injured_players (list): List of injured players from get_injury_status
        
    Returns:
        dict: Analysis of injury impacts
    """
    impact_analysis = {
        'high_risk': [],  # Out, IR, Doubtful
        'medium_risk': [], # Questionable
        'monitor': []     # Probable, Minor injuries
    }
    
    for player in injured_players:
        status = player['injury_status'].lower() if player['injury_status'] else ''
        
        if status in ['out', 'ir', 'doubtful', 'suspended']:
            impact_analysis['high_risk'].append(player)
        elif status in ['questionable', 'limited']:
            impact_analysis['medium_risk'].append(player)
        elif status in ['probable', 'healthy', 'gtd']:
            impact_analysis['monitor'].append(player)
        else:
            impact_analysis['medium_risk'].append(player)  # Unknown status
    
    return impact_analysis

def print_injury_report(injured_players):
    """
    Print a formatted injury report.
    
    Args:
        injured_players (list): List of injured players
    """
    if not injured_players:
        print("✅ No injury concerns for your roster players!")
        return
    
    print(f"\n🚑 INJURY REPORT ({len(injured_players)} players)")
    print("=" * 50)
    
    impact_analysis = analyze_injury_impact(injured_players)
    
    if impact_analysis['high_risk']:
        print("\n🔴 HIGH RISK - Consider Dropping/Benching:")
        for player in impact_analysis['high_risk']:
            print(f"❌ {player['name']} ({player['position']}) - {player['team']}")
            print(f"   Status: {player['injury_status']}")
            if player['injury_body_part']:
                print(f"   Injury: {player['injury_body_part']}")
            if player['injury_notes']:
                print(f"   Notes: {player['injury_notes'][:100]}...")
    
    if impact_analysis['medium_risk']:
        print("\n🟡 MEDIUM RISK - Monitor Closely:")
        for player in impact_analysis['medium_risk']:
            print(f"⚠️  {player['name']} ({player['position']}) - {player['team']}")
            print(f"   Status: {player['injury_status']}")
            if player['injury_body_part']:
                print(f"   Injury: {player['injury_body_part']}")
    
    if impact_analysis['monitor']:
        print("\n🟢 LOW RISK - Keep on Roster:")
        for player in impact_analysis['monitor']:
            print(f"✅ {player['name']} ({player['position']}) - {player['team']}")
            print(f"   Status: {player['injury_status']}")

def get_team_injury_context(team_abbr, all_players):
    """
    Get injury context for an entire team to identify handcuff opportunities.
    
    Args:
        team_abbr (str): Team abbreviation (e.g., 'BUF', 'KC')
        all_players (dict): Complete NFL player database
        
    Returns:
        list: Team players with injury information
    """
    team_injuries = []
    
    for player_id, player_info in all_players.items():
        if (player_info.get('team') == team_abbr and 
            player_info.get('injury_status') and 
            player_info.get('injury_status').lower() != 'healthy'):
            
            name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip()
            team_injuries.append({
                'name': name,
                'position': player_info.get('position', 'N/A'),
                'injury_status': player_info.get('injury_status'),
                'injury_body_part': player_info.get('injury_body_part', ''),
                'fantasy_positions': player_info.get('fantasy_positions', [])
            })
    
    return team_injuries