#!/usr/bin/env python3
"""
Sleeper API integration for fantasy football analysis.
Fetches user information and league data from Sleeper API.
"""

import requests
import json
from typing import Dict, List, Optional
import sys


class SleeperAPI:
    """Client for interacting with the Sleeper API."""
    
    BASE_URL = "https://api.sleeper.app/v1"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_user(self, username: str) -> Optional[Dict]:
        """
        Get user information by username.
        
        Args:
            username: Sleeper username (with or without @ prefix)
            
        Returns:
            User data dictionary or None if not found
        """
        # Remove @ prefix if present
        clean_username = username.lstrip('@')
        
        url = f"{self.BASE_URL}/user/{clean_username}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user data: {e}")
            return None
    
    def get_user_leagues(self, user_id: str, sport: str = "nfl", season: str = "2024") -> Optional[List[Dict]]:
        """
        Get leagues for a user.
        
        Args:
            user_id: Sleeper user ID
            sport: Sport type (default: "nfl")
            season: Season year (default: "2024")
            
        Returns:
            List of league data dictionaries or None if error
        """
        url = f"{self.BASE_URL}/user/{user_id}/leagues/{sport}/{season}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching leagues: {e}")
            return None


def get_demo_data():
    """Get demo data when API is not accessible."""
    return {
        'user': {
            'username': 'ryanmcpeck',
            'display_name': 'Ryan McPeck',
            'user_id': 'demo_user_id_123',
            'avatar': 'abc123'
        },
        'leagues': [
            {
                'name': 'Family League 2024',
                'league_id': 'demo_league_1',
                'status': 'in_season',
                'season': '2024',
                'total_rosters': 12,
                'scoring_type': 'ppr'
            },
            {
                'name': 'Work League',
                'league_id': 'demo_league_2', 
                'status': 'in_season',
                'season': '2024',
                'total_rosters': 10,
                'scoring_type': 'half_ppr'
            }
        ]
    }


def main():
    """Main function to fetch and display Sleeper data for @ryanmcpeck."""
    api = SleeperAPI()
    username = "ryanmcpeck"
    use_demo = "--demo" in sys.argv
    
    if use_demo:
        print(f"Using demo data for @{username}...")
        demo_data = get_demo_data()
        user_data = demo_data['user']
        leagues = demo_data['leagues']
    else:
        print(f"Fetching Sleeper data for @{username}...")
        
        # Get user information
        user_data = api.get_user(username)
        if not user_data:
            print(f"Could not find user: @{username}")
            print("Note: Use --demo flag to see sample data if API is not accessible")
            return
        
        # Get user's leagues for 2024 season
        user_id = user_data.get('user_id')
        leagues = None
        if user_id:
            leagues = api.get_user_leagues(user_id)
    
    # Display user information
    print("\n=== User Information ===")
    print(f"Username: {user_data.get('username', 'N/A')}")
    print(f"Display Name: {user_data.get('display_name', 'N/A')}")
    print(f"User ID: {user_data.get('user_id', 'N/A')}")
    print(f"Avatar: {user_data.get('avatar', 'N/A')}")
    
    # Display leagues information
    if leagues:
        print(f"\n=== Leagues (2024 NFL Season) ===")
        print(f"Total leagues: {len(leagues)}")
        
        for i, league in enumerate(leagues, 1):
            print(f"\nLeague {i}:")
            print(f"  Name: {league.get('name', 'N/A')}")
            print(f"  League ID: {league.get('league_id', 'N/A')}")
            print(f"  Status: {league.get('status', 'N/A')}")
            print(f"  Season: {league.get('season', 'N/A')}")
            print(f"  Total Rosters: {league.get('total_rosters', 'N/A')}")
            print(f"  Scoring Type: {league.get('scoring_type', 'N/A')}")
    else:
        print("\nNo leagues found for 2024 season")
    
    # Save data to JSON file
    output_data = {
        'user': user_data,
        'leagues': leagues if leagues else []
    }
    
    with open('sleeper_data.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nData saved to sleeper_data.json")


if __name__ == "__main__":
    main()