# Fantasy Football 2025 Analysis Repository

A comprehensive toolkit for analyzing and creating dashboards for your 2025 fantasy football league.

## 🏈 Features

- **Interactive Dashboard**: Streamlit-based web dashboard for league visualization
- **Data Analysis Tools**: Python utilities for fantasy football analytics
- **Flexible Data Import**: Support for CSV imports and manual data entry
- **League Configuration**: Customizable settings for different league formats
- **Multiple Analysis Views**:
  - League overview and standings
  - Team performance analysis
  - Player statistics and rankings
  - Matchup predictions
  - Waiver wire analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ryan-mcpeck/fantasy-football-2025.git
cd fantasy-football-2025
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Initialize sample data (optional):
```bash
python src/data_importer.py
```

4. Configure your league settings:
```bash
# Edit config/league_config.json with your league details
```

### Running the Dashboard

```bash
streamlit run dashboards/main_dashboard.py
```

The dashboard will open in your web browser at `http://localhost:8501`

## 📁 Project Structure

```
fantasy-football-2025/
├── config/                 # Configuration files
│   └── league_config.json # League settings
├── data/                   # Data storage
│   ├── teams.csv          # Team data
│   ├── players.csv        # Player statistics
│   └── matchups.csv       # Game results
├── dashboards/             # Dashboard applications
│   └── main_dashboard.py  # Main Streamlit dashboard
├── notebooks/              # Jupyter notebooks for analysis
├── src/                    # Source code
│   ├── fantasy_analyzer.py # Analysis functions
│   └── data_importer.py   # Data import utilities
├── tests/                  # Test files
└── requirements.txt        # Python dependencies
```

## 🔧 Configuration

### League Settings

Edit `config/league_config.json` to customize:

- League name and format (PPR, Standard, etc.)
- Number of teams and playoff structure
- Roster composition and scoring settings
- Data import preferences

### Data Import

**CSV Import:**
1. Use the template files in `data/` folder
2. Update with your league data
3. Import via the dashboard or Python scripts

**Manual Entry:**
- Use the dashboard interface for quick updates
- Suitable for weekly score entry

## 📊 Analysis Features

### Power Rankings
- Advanced team ranking system
- Combines wins and points-per-game
- Weekly trend analysis

### Matchup Predictions
- Statistical matchup analysis
- Win probability calculations
- Performance-based forecasting

### Player Analysis
- Position rankings and comparisons
- Sleeper and bust identification
- Waiver wire recommendations

### Playoff Scenarios
- Real-time playoff probability
- Clinching and elimination scenarios
- Bracket predictions

## 🧪 Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/ dashboards/
flake8 src/ dashboards/
```

### Adding New Features

1. Create new analysis functions in `src/fantasy_analyzer.py`
2. Add dashboard pages in `dashboards/main_dashboard.py`
3. Update configuration in `config/league_config.json` if needed
4. Add tests in `tests/` directory

## 📈 Usage Examples

### Basic Analysis
```python
from src.fantasy_analyzer import FantasyAnalyzer
from src.data_importer import load_team_data

# Initialize analyzer
analyzer = FantasyAnalyzer()

# Load your data
teams_df = load_team_data('data/teams.csv')

# Generate power rankings
rankings = analyzer.calculate_power_rankings(teams_df)
print(rankings)
```

### Matchup Prediction
```python
# Predict matchup between two teams
team1_data = teams_df[teams_df['team_name'] == 'Team Alpha'].iloc[0]
team2_data = teams_df[teams_df['team_name'] == 'Team Beta'].iloc[0]

prediction = analyzer.predict_matchup(team1_data, team2_data)
print(f"Predicted winner: {prediction['predicted_winner']}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the dashboard interface
- Uses [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/) for data analysis
- Visualizations powered by [Plotly](https://plotly.com/python/)

## 🔮 Roadmap

- [ ] API integration with major fantasy platforms (ESPN, Yahoo, Sleeper)
- [ ] Advanced machine learning predictions
- [ ] Mobile-responsive dashboard improvements
- [ ] Automated weekly data updates
- [ ] Advanced trade analysis tools
- [ ] Historical season comparisons
- [ ] Email/SMS notifications for important updates

---

**Happy analyzing! 🏈📊**
