#!/usr/bin/env python3
"""
Simple tests for the Sleeper API integration.
"""

import unittest
from unittest.mock import Mock, patch
import json
import os
from sleeper_api import SleeperAPI, get_demo_data


class TestSleeperAPI(unittest.TestCase):
    """Test cases for SleeperAPI class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api = SleeperAPI()
    
    def test_demo_data_structure(self):
        """Test that demo data has the expected structure."""
        demo_data = get_demo_data()
        
        # Test user data structure
        self.assertIn('user', demo_data)
        user = demo_data['user']
        self.assertIn('username', user)
        self.assertIn('display_name', user)
        self.assertIn('user_id', user)
        self.assertIn('avatar', user)
        self.assertEqual(user['username'], 'ryanmcpeck')
        
        # Test leagues data structure
        self.assertIn('leagues', demo_data)
        leagues = demo_data['leagues']
        self.assertIsInstance(leagues, list)
        self.assertGreater(len(leagues), 0)
        
        # Test first league structure
        league = leagues[0]
        self.assertIn('name', league)
        self.assertIn('league_id', league)
        self.assertIn('status', league)
        self.assertIn('season', league)
        self.assertIn('total_rosters', league)
        self.assertIn('scoring_type', league)
    
    @patch('sleeper_api.requests.Session.get')
    def test_get_user_success(self, mock_get):
        """Test successful user retrieval."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'username': 'ryanmcpeck',
            'display_name': 'Ryan McPeck',
            'user_id': '123456',
            'avatar': 'avatar_hash'
        }
        mock_get.return_value = mock_response
        
        result = self.api.get_user('ryanmcpeck')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], 'ryanmcpeck')
        self.assertEqual(result['display_name'], 'Ryan McPeck')
    
    @patch('sleeper_api.requests.Session.get')
    def test_get_user_with_at_symbol(self, mock_get):
        """Test that @ symbol is properly stripped from username."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'username': 'ryanmcpeck'}
        mock_get.return_value = mock_response
        
        self.api.get_user('@ryanmcpeck')
        
        # Verify the URL called doesn't include the @
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn('/user/ryanmcpeck', args[0])
    
    @patch('sleeper_api.requests.Session.get')
    def test_get_user_failure(self, mock_get):
        """Test user retrieval failure."""
        # Mock failed API response
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("API Error")
        
        result = self.api.get_user('nonexistentuser')
        
        self.assertIsNone(result)
    
    @patch('sleeper_api.requests.Session.get')
    def test_get_user_leagues_success(self, mock_get):
        """Test successful leagues retrieval."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                'name': 'Test League',
                'league_id': 'test_league_1',
                'status': 'in_season'
            }
        ]
        mock_get.return_value = mock_response
        
        result = self.api.get_user_leagues('123456')
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Test League')


if __name__ == '__main__':
    # Clean up any existing test files
    if os.path.exists('sleeper_data.json'):
        os.remove('sleeper_data.json')
    
    unittest.main()