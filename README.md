# fantasy-football-2025
Analysis of 2025 fantasy football league

## Sleeper API Integration

This project includes functionality to pull fantasy football data from the Sleeper API for user @ryanmcpeck.

### Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Fetch Real Data from Sleeper API
```bash
python sleeper_api.py
```

#### Use Demo Data (when API is not accessible)
```bash
python sleeper_api.py --demo
```

### Features

- Fetches user profile information from Sleeper API
- Retrieves all leagues for the 2024 NFL season
- Saves data to `sleeper_data.json` for further analysis
- Includes demo mode for testing when API is not accessible

### Output

The script displays:
- User information (username, display name, user ID, avatar)
- League information (name, ID, status, roster count, scoring type)
- Saves all data to `sleeper_data.json`

### API Endpoints Used

- `GET /v1/user/{username}` - Get user information
- `GET /v1/user/{user_id}/leagues/nfl/{season}` - Get user's leagues

For more information about the Sleeper API, visit: https://docs.sleeper.app/
