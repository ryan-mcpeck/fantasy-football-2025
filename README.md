# Fantasy Football 2025 - GitHub Gridiron 🏈

AI-powered fantasy football analysis and waiver wire assistant for the 2025 season.

## 🎯 About

This project uses the Sleeper API to analyze fantasy football leagues and provide data-driven waiver wire recommendations. Built as an AI-assisted fantasy football experiment for the "GitHub Gridiron" team.

## 🚀 Features

- **Quick Scan Mode**: Daily trending player analysis (perfect for morning checks)
- **Full Analysis Mode**: Comprehensive roster evaluation with position-specific swap suggestions
- **Trending Drops Detection**: Alerts when your players are being dropped frequently
- **Real-time Data**: Uses Sleeper API for up-to-date trending player information
- **Smart Filtering**: Only shows players actually available in your specific league
- **Rate Limiting Protection**: Respects Sleeper API limits with built-in safeguards

## 📋 Requirements

- Python 3.7+
- `requests` library
- Sleeper fantasy football account

## ⚙️ Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ryan-mcpeck/fantasy-football-2025.git
   cd fantasy-football-2025
   ```

2. **Set up Python environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install requests
   ```

3. **Configure your settings**
   - Open `fantasy_waiver_assistant.py`
   - Update `USERNAME` with your Sleeper username
   - Update `SEASON` if needed (defaults to 2025)

## 🎮 Usage

### Quick Daily Check
```bash
python fantasy_waiver_assistant.py
# or
python fantasy_waiver_assistant.py quick
```
Perfect for daily morning checks to catch trending players early.

### Full Roster Analysis
```bash
python fantasy_waiver_assistant.py full
```
Comprehensive analysis with detailed swap recommendations. Best used before waiver deadlines.

### Help
```bash
python fantasy_waiver_assistant.py help
```

## 📊 Example Output

### Quick Scan
```
🏈 GitHub Gridiron - AI Fantasy Assistant
========================================

⚡ QUICK SCAN - 2025-09-09 20:45
==================================================
Fetching trending players...

🔥 HOT PICKUPS RIGHT NOW:
1. Calvin Austin (WR) - PIT - 1,691,811 adds
2. Harold Fannin (TE) - CLE - 1,641,705 adds
3. Kenneth Gainwell (RB) - PIT - 751,328 adds

⚠️  YOUR PLAYERS BEING DROPPED:
❌ Problem Player (WR) - NYJ - 45,000 drops
Consider cutting these players before they lose more value!

✅ None of your other players are trending downward.
```

### Full Analysis
```
📋 YOUR ROSTER (17 players):
QB: Brock Purdy (SF), Geno Smith (LV)
RB: Breece Hall (NYJ), D'Andre Swift (CHI)
WR: Garrett Wilson (NYJ), Terry McLaurin (WAS), Problem Player (NYJ) ⚠️

⚠️  ROSTER ALERTS - Players Being Dropped:
❌ Problem Player (WR) - NYJ - 45,000 drops
💡 Consider cutting these players for trending adds!

🔄 SWAP RECOMMENDATIONS:
WR Options:
  ⬆️  Calvin Austin (PIT) - 1,691,811 adds
  Your WRs: Garrett Wilson, Terry McLaurin
```

## 🤖 AI Integration

This project leverages AI assistance for:
- Data analysis and interpretation
- Code optimization and documentation
- Strategic waiver wire recommendations
- Fantasy football trend analysis
- Roster management alerts (trending drops detection)
- Rate limiting and API best practices

## 📁 Project Structure

```
fantasy-football-2025/
├── fantasy_waiver_assistant.py    # Main analysis script
├── .venv/                         # Python virtual environment
└── README.md                      # This file
```

## 🔧 Customization

The script can be easily modified to:
- Target multiple leagues
- Adjust trending time windows
- Filter by specific positions
- Add custom scoring analysis
- Modify rate limiting settings
- Set up automated alerts

## 📈 Tips for Success

1. **Run quick scans daily** - Catch breakout players before others
2. **Use full analysis before waivers** - Make strategic roster decisions
3. **Monitor trending counts** - Higher counts indicate stronger consensus
4. **Watch for drop alerts** - Cut players before they lose more value
5. **Focus on position needs** - Target areas where your roster is weakest
6. **Act fast on high-volume trends** - Players with 500K+ adds are likely must-haves

## 🏆 About GitHub Gridiron

"GitHub Gridiron" represents the fusion of AI-powered analysis with traditional fantasy football strategy. This project showcases how modern tools can enhance fantasy sports decision-making through:

- **Predictive Analytics**: Using crowd wisdom (trending data) to predict player value
- **Risk Management**: Early warning system for dropping player values  
- **Automated Insights**: AI-driven recommendations for roster optimization
- **Data-Driven Decisions**: Objective analysis over gut feelings

The project demonstrates practical AI application in sports analytics, combining real-time data processing with strategic decision-making algorithms.

## 🔨 Development Guidelines

### For Contributors & AI Assistance
- **Always update README.md** when adding features or making significant changes
- Maintain comprehensive code documentation with docstrings and comments
- Follow rate limiting best practices for API calls
- Test new features thoroughly before committing
- Keep user experience and practical utility as top priorities
- Use descriptive variable names and clear function organization

### Code Standards
- Add step-by-step comments for complex logic
- Include error handling with user-friendly messages
- Maintain consistent naming conventions throughout
- Document all functions with purpose, parameters, and return values

## 📝 License

This project is open source and available under the MIT License.

---

*Built with AI assistance • Powered by Sleeper API • Go GitHub Gridiron! 🚀*
