import ranking as rk
import datetime as dt
from helper import get_outcome_from_file


class Game(object):

    def __init__(self):

        self.game = None
        self.season = None
        self.league = None
        self.hteam = None
        self.ateam = None
        self.date_dt = None
        self.features = None
        self.outcome = None

    def __call__(self, game, season, league, date_dt):

        self.game = game
        self.hteam = game[0]
        self.ateam = game[1]
        self.season = season
        self.league = league
        self.date_dt = date_dt

        self.features = self._get_all_features()

        self.outcome = self._get_outcome_of_game()

    def _get_all_features(self):
        # Get the several features
        features = []

        features.extend(self._get_rank())

        return features

    def _get_outcome_of_game(self):

        if self.date_dt < dt.date.today():
            # historical data to lookup in right csv
            historical_outcome = get_outcome_from_file(
                self.hteam, self.ateam, self.season, self.league)
            return historical_outcome
        else:
            # Game has not been played yet: prediction expected
            return 'P'

    """
    Feature getters
    """

    def _get_rank(self):
        # Get the current rank in the league for both teams
        current_ranking = rk.Ranking()
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        rank_h = current_ranking.table[self.hteam]['position']
        # Away team
        rank_a = current_ranking.table[self.ateam]['position']

        ranks = [rank_h, rank_a]
        return ranks

    def _get_final_rank_previous_season(self):
        # Get the final rank for the 2 previous seasons
        return []

    def _get_budget_season(self):
        # Get the buget of the teams for the season
        return []

    def _get_nb_games_with_coach(self):
        # Nb of games with same coach/manager
        return []

    def _get_last_outcomes_away(self):
        # Get 5, 10 last outcomes for both teams when away
        return []

    def _get_last_outcomes_home(self):
        # Get 5, 10 last outcomes for both teams when home
        return []

    def _get_nb_goals_scored_previous_game(self):
        # Get last game stats for both teams
        # goals or other stats...
        return []


