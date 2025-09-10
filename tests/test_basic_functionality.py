#!/usr/bin/env python3
"""
Basic tests for fantasy football analysis functionality
"""

import sys
import os
import pytest
import pandas as pd

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fantasy_analyzer import FantasyAnalyzer, load_team_data, load_player_data
from data_importer import DataImporter


def test_fantasy_analyzer_initialization():
    """Test that FantasyAnalyzer can be initialized"""
    analyzer = FantasyAnalyzer()
    assert analyzer is not None
    assert isinstance(analyzer.config, dict)


def test_load_team_data():
    """Test loading team data"""
    teams_df = load_team_data()
    assert isinstance(teams_df, pd.DataFrame)
    assert len(teams_df) > 0
    
    required_columns = ['team_name', 'owner', 'wins', 'losses', 'points_for']
    for col in required_columns:
        assert col in teams_df.columns


def test_load_player_data():
    """Test loading player data"""
    players_df = load_player_data()
    assert isinstance(players_df, pd.DataFrame)
    assert len(players_df) > 0
    
    required_columns = ['player_name', 'position', 'points']
    for col in required_columns:
        assert col in players_df.columns


def test_power_rankings():
    """Test power rankings calculation"""
    analyzer = FantasyAnalyzer()
    teams_df = load_team_data()
    
    rankings = analyzer.calculate_power_rankings(teams_df)
    assert isinstance(rankings, pd.DataFrame)
    assert 'power_rank' in rankings.columns
    assert 'power_score' in rankings.columns
    
    # Check that rankings are sorted correctly
    assert rankings['power_rank'].tolist() == list(range(1, len(rankings) + 1))


def test_matchup_prediction():
    """Test matchup prediction functionality"""
    analyzer = FantasyAnalyzer()
    teams_df = load_team_data()
    
    team1_data = teams_df.iloc[0].to_dict()
    team2_data = teams_df.iloc[1].to_dict()
    
    prediction = analyzer.predict_matchup(team1_data, team2_data)
    
    assert isinstance(prediction, dict)
    assert 'team1_win_probability' in prediction
    assert 'team2_win_probability' in prediction
    assert 'predicted_winner' in prediction
    assert 'confidence' in prediction
    
    # Probabilities should sum to 1
    prob_sum = prediction['team1_win_probability'] + prediction['team2_win_probability']
    assert abs(prob_sum - 1.0) < 0.001


def test_playoff_scenarios():
    """Test playoff scenarios calculation"""
    analyzer = FantasyAnalyzer()
    teams_df = load_team_data()
    
    scenarios = analyzer.playoff_scenarios(teams_df)
    
    assert isinstance(scenarios, dict)
    assert 'current_playoff_teams' in scenarios
    assert 'bubble_teams' in scenarios
    assert 'clinched' in scenarios
    assert 'eliminated' in scenarios


def test_data_importer():
    """Test data importer functionality"""
    importer = DataImporter()
    assert importer is not None
    
    # Test sample data creation
    sample_data = importer.create_sample_data()
    assert isinstance(sample_data, dict)
    assert 'teams' in sample_data
    assert 'players' in sample_data
    assert 'matchups' in sample_data


def test_data_validation():
    """Test data validation functionality"""
    importer = DataImporter()
    teams_df = load_team_data()
    
    validation = importer.validate_data(teams_df, 'teams')
    assert isinstance(validation, dict)
    assert 'valid' in validation
    assert 'issues' in validation


if __name__ == "__main__":
    # Run tests if called directly
    pytest.main([__file__, "-v"])