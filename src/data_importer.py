#!/usr/bin/env python3
"""
Data Import Utilities
Tools for importing fantasy football data from various sources
"""

import pandas as pd
import requests
import json
import csv
from typing import Dict, List, Optional, Union
import os
from datetime import datetime


class DataImporter:
    """Class for importing fantasy football data from various sources"""

    def __init__(self, config_path: str = "config/league_config.json"):
        """Initialize with configuration"""
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    def import_from_csv(self, file_path: str, data_type: str) -> pd.DataFrame:
        """Import data from CSV file"""
        try:
            df = pd.read_csv(file_path)

            # Validate required columns based on data type
            if data_type == "teams":
                required_cols = ["team_name", "owner", "wins", "losses", "points_for"]
                if not all(col in df.columns for col in required_cols):
                    raise ValueError(f"CSV missing required columns: {required_cols}")

            elif data_type == "players":
                required_cols = ["player_name", "position", "points"]
                if not all(col in df.columns for col in required_cols):
                    raise ValueError(f"CSV missing required columns: {required_cols}")

            return df

        except Exception as e:
            print(f"Error importing CSV: {e}")
            return pd.DataFrame()

    def export_to_csv(self, df: pd.DataFrame, file_path: str) -> bool:
        """Export DataFrame to CSV"""
        try:
            df.to_csv(file_path, index=False)
            return True
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return False

    def create_sample_data(self) -> Dict[str, pd.DataFrame]:
        """Create sample data for testing"""
        # Sample team data
        teams_data = {
            "team_name": [
                "The Touchdown Kings",
                "Gridiron Gladiators",
                "Fantasy Fanatics",
                "End Zone Elites",
                "Playbook Pirates",
                "Championship Chasers",
                "Draft Day Dynamos",
                "Victory Vultures",
                "Roster Rockets",
                "League Legends",
                "Fantasy Phenoms",
                "Playoff Predators",
            ],
            "owner": [f"Owner_{i+1}" for i in range(12)],
            "wins": [9, 8, 8, 7, 7, 6, 6, 5, 5, 4, 3, 2],
            "losses": [4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 10, 11],
            "points_for": [
                1356.8,
                1298.7,
                1267.9,
                1245.5,
                1234.6,
                1201.5,
                1189.2,
                1156.7,
                1098.2,
                1087.3,
                1021.4,
                967.3,
            ],
            "points_against": [
                1089.6,
                1167.8,
                1156.3,
                1198.3,
                1201.2,
                1178.9,
                1234.5,
                1189.4,
                1245.6,
                1278.9,
                1298.7,
                1289.7,
            ],
        }

        # Sample player data
        players_data = {
            "player_name": [
                "Josh Allen",
                "Lamar Jackson",
                "Patrick Mahomes",
                "Dak Prescott",
                "Christian McCaffrey",
                "Alvin Kamara",
                "Derrick Henry",
                "Nick Chubb",
                "Cooper Kupp",
                "Davante Adams",
                "Tyreek Hill",
                "Stefon Diggs",
                "Travis Kelce",
                "Mark Andrews",
                "George Kittle",
                "T.J. Hockenson",
            ],
            "position": [
                "QB",
                "QB",
                "QB",
                "QB",
                "RB",
                "RB",
                "RB",
                "RB",
                "WR",
                "WR",
                "WR",
                "WR",
                "TE",
                "TE",
                "TE",
                "TE",
            ],
            "team": [
                "BUF",
                "BAL",
                "KC",
                "DAL",
                "SF",
                "NO",
                "TEN",
                "CLE",
                "LAR",
                "LV",
                "MIA",
                "BUF",
                "KC",
                "BAL",
                "SF",
                "MIN",
            ],
            "points": [
                287.4,
                268.7,
                252.3,
                234.8,
                234.6,
                198.2,
                187.9,
                165.4,
                189.3,
                174.6,
                167.8,
                156.2,
                156.7,
                134.5,
                128.9,
                112.3,
            ],
            "games_played": [13, 12, 14, 13, 11, 12, 12, 10, 9, 13, 14, 12, 13, 12, 11, 13],
            "avg_points": [
                22.1,
                22.4,
                18.0,
                18.1,
                21.3,
                16.5,
                15.7,
                16.5,
                21.0,
                13.4,
                12.0,
                13.0,
                12.1,
                11.2,
                11.7,
                8.6,
            ],
        }

        # Sample matchup data
        matchups_data = {
            "week": [1, 1, 1, 2, 2, 2],
            "team1": [
                "The Touchdown Kings",
                "Gridiron Gladiators",
                "Fantasy Fanatics",
                "The Touchdown Kings",
                "End Zone Elites",
                "Playbook Pirates",
            ],
            "team2": [
                "End Zone Elites",
                "Playbook Pirates",
                "Championship Chasers",
                "Gridiron Gladiators",
                "Fantasy Fanatics",
                "Championship Chasers",
            ],
            "team1_score": [124.5, 98.7, 109.3, 132.8, 87.4, 91.2],
            "team2_score": [89.2, 112.4, 95.6, 98.9, 103.7, 88.9],
        }

        return {
            "teams": pd.DataFrame(teams_data),
            "players": pd.DataFrame(players_data),
            "matchups": pd.DataFrame(matchups_data),
        }

    def initialize_data_files(self, force_overwrite: bool = False) -> bool:
        """Initialize data files with sample data"""
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        sample_data = self.create_sample_data()

        files_created = []

        for data_type, df in sample_data.items():
            file_path = os.path.join(data_dir, f"{data_type}.csv")

            if not os.path.exists(file_path) or force_overwrite:
                if self.export_to_csv(df, file_path):
                    files_created.append(file_path)
                else:
                    print(f"Failed to create {file_path}")
                    return False

        print(f"Created sample data files: {files_created}")
        return True

    def validate_data(self, df: pd.DataFrame, data_type: str) -> Dict[str, Union[bool, List[str]]]:
        """Validate imported data"""
        issues = []

        if data_type == "teams":
            # Check for required columns
            required = ["team_name", "owner", "wins", "losses", "points_for"]
            missing = [col for col in required if col not in df.columns]
            if missing:
                issues.append(f"Missing columns: {missing}")

            # Check for negative values
            if "wins" in df.columns and (df["wins"] < 0).any():
                issues.append("Negative wins values found")
            if "losses" in df.columns and (df["losses"] < 0).any():
                issues.append("Negative losses values found")
            if "points_for" in df.columns and (df["points_for"] < 0).any():
                issues.append("Negative points_for values found")

        elif data_type == "players":
            required = ["player_name", "position", "points"]
            missing = [col for col in required if col not in df.columns]
            if missing:
                issues.append(f"Missing columns: {missing}")

            # Validate positions
            if "position" in df.columns:
                valid_positions = ["QB", "RB", "WR", "TE", "K", "DST"]
                invalid_positions = df[~df["position"].isin(valid_positions)]["position"].unique()
                if len(invalid_positions) > 0:
                    issues.append(f"Invalid positions found: {invalid_positions}")

        return {"valid": len(issues) == 0, "issues": issues}


def create_data_template(data_type: str, output_path: str) -> bool:
    """Create a CSV template for data import"""
    templates = {
        "teams": {
            "team_name": ["Team 1", "Team 2", "Team 3"],
            "owner": ["Owner 1", "Owner 2", "Owner 3"],
            "wins": [7, 6, 5],
            "losses": [6, 7, 8],
            "points_for": [1200.5, 1150.3, 1100.8],
            "points_against": [1180.2, 1170.9, 1190.4],
        },
        "players": {
            "player_name": ["Player 1", "Player 2", "Player 3"],
            "position": ["QB", "RB", "WR"],
            "team": ["BUF", "SF", "LAR"],
            "points": [250.5, 200.3, 180.7],
            "games_played": [13, 12, 11],
        },
    }

    if data_type not in templates:
        print(f"Unknown data type: {data_type}")
        return False

    try:
        df = pd.DataFrame(templates[data_type])
        df.to_csv(output_path, index=False)
        print(f"Template created: {output_path}")
        return True
    except Exception as e:
        print(f"Error creating template: {e}")
        return False


if __name__ == "__main__":
    # Example usage
    importer = DataImporter()

    # Initialize sample data
    importer.initialize_data_files()

    # Create templates
    create_data_template("teams", "data/teams_template.csv")
    create_data_template("players", "data/players_template.csv")
