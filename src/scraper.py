import soccerdata as sd
import pandas as pd

class SoccerScraper:
    def __init__(self, league='ENG-Premier League', season='2024'):
        """
        Initialize the scraper with a specific league and season.
        
        Args:
            league (str): The league to scrape (e.g., 'ENG-Premier League').
            season (str): The season to scrape (e.g., '2024' for 2024-2025).
        """
        self.league = league
        self.season = season
        self.fbref = sd.FBref(leagues=league, seasons=season)

    def get_schedule(self):
        """
        Fetch the schedule for the season.
        """
        return self.fbref.read_schedule()

    def get_team_season_stats(self, stat_type="passing"):
        """
        Fetch team season statistics.
        
        Args:
            stat_type (str): The type of stats to fetch (default: "passing").
        """
        return self.fbref.read_team_season_stats(stat_type=stat_type)

    def get_player_season_stats(self, stat_type="standard"):
        """
        Fetch player season statistics.
        
        Args:
            stat_type (str): The type of stats to fetch (default: "standard").
        """
        return self.fbref.read_player_season_stats(stat_type=stat_type)
