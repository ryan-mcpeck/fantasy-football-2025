# FantasyAI Pro - Advanced Fantasy Football Analysis Suite 🤖

AI-powered fantasy football analysis combining trending data, performance analytics, and strategic planning for the 2025 season.

## 🎯 About

FantasyAI Pro is an advanced fantasy football analysis tool that uses the Sleeper API to provide data-driven roster optimization. Built as an AI-assisted fantasy football experiment for the "GitHub Gridiron" team, combining multiple analysis modes for comprehensive roster management.

## 🚀 Features

- **Quick Scan Mode**: Daily trending player analysis (perfect for morning checks)
- **Full Analysis Mode**: Comprehensive roster evaluation with position-specific swap suggestions
- **Performance Analytics**: Track actual fantasy points to identify underperforming players
- **Visual Performance Charts**: Weekly point charts showing trends for each roster player
- **Enhanced Analysis**: NEW! Integrated injury tracking and trade target analysis
- **Lineup Optimizer**: NEW! Compare bench vs starters with performance-based recommendations
- **Weekly Game Plan Generator**: Comprehensive strategy planning after games complete
- **Trending Analysis**: Real-time player movement tracking (adds/drops)
- **Smart Filtering**: Only shows players actually available in your specific league
- **AI-Powered Insights**: Data-driven recommendations for optimal roster decisions

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
   - Open `fantasyai_pro.py`
   - Update `USERNAME` with your Sleeper username
   - Update `SEASON` if needed (defaults to 2025)

## 🎮 Usage

### Quick Daily Check
```bash
python fantasyai_pro.py
# or
python fantasyai_pro.py quick
```
Perfect for daily morning checks to catch trending players early.

### Full Roster Analysis
```bash
python fantasyai_pro.py full
```
Comprehensive analysis with detailed swap recommendations. Best used before waiver deadlines.

### Performance Analysis
```bash
python fantasyai_pro.py performance
```
Analyzes actual fantasy points scored to identify consistently underperforming players.

### Visual Performance Chart
```bash
python fantasyai_pro.py chart
```
Creates visual charts showing weekly fantasy points for each player over recent weeks.

### Enhanced Analysis with Injury & Trade Intelligence
```bash
python fantasyai_pro.py enhanced
```
Comprehensive analysis combining injury reports, trade targets, and strategic recommendations.

### Lineup Optimizer (Performance-Based)
```bash
python fantasyai_pro.py lineup
```
Analyzes recent performance to recommend optimal starting lineup and identify bench players outperforming starters.

### Weekly Game Plan
```bash
python fantasyai_pro.py gameplan
```
Generates comprehensive weekly strategy with prioritized actions and schedules.

### Help
```bash
python fantasyai_pro.py help
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

### Performance Analysis
```
📈 PERFORMANCE ANALYSIS - 2025-11-16 21:30
============================================================

📊 PERFORMANCE ANALYSIS - Last 3 Weeks (Weeks 9-11)
------------------------------------------------------------
⚠️  UNDERPERFORMING PLAYERS (< 8.0 pts):
❌ Jerry Jeudy (WR) - CLE - 3/3 weeks below threshold
   Recent poor weeks: 2.4, 1.8 pts
❌ Calvin Austin (WR) - PIT - 2/3 weeks below threshold
   Recent poor weeks: 3.1, 0.6 pts

💡 RECOMMENDATION: Consider dropping players with 2+ poor weeks for trending adds!

🏆 PERFORMANCE CONTEXT:
Consider combining this analysis with trending data for optimal decisions.
Players can have good underlying performance but still be droppable if better options emerge.
```

### Visual Performance Chart
```
📈 PERFORMANCE ANALYSIS - 2025-11-16 23:45
============================================================
Loading player data and analyzing recent performance...

📊 PERFORMANCE ANALYSIS - Last 3 Weeks (Weeks 9-11)
------------------------------------------------------------
✅ No players consistently underperforming (below 8.0 pts)
Your roster is performing well from a points perspective!

📊 Generating performance chart...
📈 Performance chart saved as: weekly_performance_chart_20251116_2345.png
📈 Chart shows weekly fantasy points for each player over recent weeks
🔴 Red dashed line shows poor performance threshold (8.0 pts)
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
├── fantasyai_pro.py               # Main analysis script
├── charts/                        # Generated performance charts
├── .copilot-instructions.md       # AI development guidelines
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

## 💡 Weekly Success Workflow

1. **Monday Night**: Run `gameplan` after games complete to get weekly strategy
2. **Tuesday Morning**: Run `quick` to catch early trending players
3. **Tuesday Evening**: Execute drops and claims based on game plan
4. **Wednesday**: Run `full` analysis to review waiver results
5. **Thursday**: Run `performance` to validate roster decisions
6. **Weekend**: Generate `chart` for visual performance tracking
7. **Sunday**: Set optimal lineup based on all analysis

### Daily Maintenance:
- **Morning**: `quick` scan for trending opportunities
- **Evening**: Monitor player news and injury reports
- **Weekly**: Full performance review with charts

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
