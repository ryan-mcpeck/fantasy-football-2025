#!/usr/bin/env python3
"""
Fantasy Football 2025 Dashboard Launcher
Simple launcher script for the Streamlit dashboard
"""

import subprocess
import sys
import os


def main():
    """Launch the fantasy football dashboard"""
    # Check if we're in the right directory
    if not os.path.exists("dashboards/main_dashboard.py"):
        print("Error: Please run this script from the fantasy-football-2025 directory")
        print("Expected to find 'dashboards/main_dashboard.py'")
        return 1
    
    # Check if required packages are installed
    try:
        import streamlit
        import pandas
        import plotly
    except ImportError as e:
        print(f"Error: Missing required package: {e}")
        print("Please install requirements with: pip install -r requirements.txt")
        return 1
    
    # Launch Streamlit dashboard
    print("🏈 Launching Fantasy Football 2025 Dashboard...")
    print("The dashboard will open in your web browser at http://localhost:8501")
    print("Press Ctrl+C to stop the dashboard")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboards/main_dashboard.py",
            "--server.headless", "false",
            "--server.runOnSave", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Thanks for using Fantasy Football 2025 Dashboard!")
    except Exception as e:
        print(f"Error launching dashboard: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())