__author__ = "Dimitar Ganev"
__email__ = "<dganev@pm.me>"

import requests
from typing import List, Dict
from datetime import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta, SU, SA

class OpenLigaSDK:
    """
    https://www.openligadb.de/
    -------------------------
    OpenLigaDB is providing an open database for recent football seasons and
    matches The project is aimed primarily at (hobby) programmers who want to
    obtain current soccer and other sports results in their applications.
    The interface is particularly suitable for the implementation of projects
    for prediction games, statistic applications, Bundesliga widgets etc..
    """

    def __init__(self):
        self.api_url = "https://www.openligadb.de/api/"

    def get_season(self, season: str, reverse: bool = False) -> List:
        """
        Args:
            season: the season (ex. 2017, 2018 etc..)
        Returns:
            A List showing the matches for that season.
        """
        route = self.api_url + "/getmatchdata/bl1/" + season
        data = requests.get(route)
        if reverse:
            return data.json()[::-1]
        return data.json()

    def get_rankings(self, season: str) -> Dict:
        """
        Getting the ranked for the given season.

        Args:
            season: (str): the season (ex. 2017, 2018 etc..)
        Returns:
            A dictionary showing the rankings for that season.
        """
        # Getting the current teams in the season.
        teams = self.get_teams(season)
        rankings = {}

        for team in teams:
            rankings[team["TeamId"]] = {
                "team_name": team["TeamName"],
                "wins": 0,
                "loses": 0,
                "draws": 0,
                "points": 0,
            }

        # Getting the current Season
        season = self.get_season(season)

        for match in season:
            if not match["MatchIsFinished"]:
                continue

            team_1 = match["Team1"]["TeamId"]
            team_2 = match["Team2"]["TeamId"]

            if match["MatchResults"]:
                goals_team_1 = int(match["MatchResults"][0]["PointsTeam1"])
                goals_team_2 = int(match["MatchResults"][0]["PointsTeam2"])

                # if TEAM 1 has won the match.
                if goals_team_1 > goals_team_2:
                    rankings[team_1]["wins"] += 1
                    rankings[team_1]["points"] += 3
                    rankings[team_2]["loses"] += 1
                # if TEAM 2 has won the match.
                elif goals_team_1 < goals_team_2:
                    rankings[team_2]["wins"] += 1
                    rankings[team_2]["points"] += 3
                    rankings[team_1]["loses"] += 1
                # if it is a draw
                else:
                    rankings[team_1]["points"] += 1
                    rankings[team_2]["points"] += 1
                    rankings[team_1]["draws"] += 1
                    rankings[team_2]["draws"] += 1

        return self._sort(rankings)

    def _sort(self, rankings: Dict) -> Dict:
        """
        Sorting the current rankings based on the points.

        Args:
            rankings: the returning rankings which get_rankings() returns.
        Returns:
            A sorted rankings Dictionary.
        """
        return sorted(
            [v for k, v in rankings.items()], key=lambda x: x["points"], reverse=True
        )

    def get_teams(self, season: str) -> List:
        """
        Args:
            season: the season (ex. 2017, 2018 etc..)
        Returns:
            A list with the teams playing in that season.
        """
        route = self.api_url + "/getavailableteams/bl1/" + season
        data = requests.get(route)
        return data.json()

    def get_weekend_matches(self, season: str) -> List:
        """
        Args:
            season: the season (ex. 2017, 2018 etc..)
        Returns:
            A List with the upcoming matches (if theres any), otherwise
            None would be given.
        """
        current_season = self.get_season(season)
        weekdays = self._get_current_week_weekdays_dates()
        result = []

        for match in current_season:
            try:
                match_play_date = self._parse_date(match["MatchDateTime"])
            except ValueError:
                raise ValueError("Invalid DateTime Format: [MatchDateTime]")
            if match_play_date == weekdays["SA"] or match_play_date == weekdays["SU"]:
                result.append(match)
        return result if result else None

    def search_team(self, search: str, season: str) -> List:
        """
        Searching for a team by a given string (search).

        Args:
            search: the search string (team name)
            season: the season (ex. 2017, 2018 etc..)
        Returns:
            A list with all results which matched the search.
        """
        teams = self.get_teams(season)
        return [i for i in teams if search.lower() in i["TeamName"].lower()]

    @staticmethod
    def _parse_date(date) -> datetime:
        """
        Parsing a date, replacing its 'time' values so that it can be comprabale
        with _get_current_week_weekdays_dates()
        Returns:
            A datetime.datetime object.
        """
        # https://dateutil.readthedocs.io/en/stable/parser.html
        return parser.parse(date).replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def _get_current_week_weekdays_dates() -> Dict:
        """
        Returns: Dict, the current weekdays as datetime objects.
        """
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # MOCK
        # now = parser.parse("2019-04-22 00:00:00")

        # Getting the current weekend days.
        sunday = now + relativedelta(weekday=SU)
        saturday = now + relativedelta(weekday=SA)

        # Probably SAT/SUN would be better but I deciced to keep it consistant
        # with the decisions by dateutils
        return {"SA": saturday, "SU": sunday}
