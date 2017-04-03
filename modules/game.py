import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)
import ranking as rk
import datetime as dt
from helper import get_outcome_from_file
import pandas as pd
from constants import SEASONS, SEASONS_INDEX


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
        rank_h = current_ranking.table.loc[self.hteam, 'Pos']
        # Away team
        rank_a = current_ranking.table.loc[self.hteam, 'Pos']

        ranks = [rank_h, rank_a]
        return ranks

    def _get_final_rank_previous_season(self):
        season_index = SEASONS[self.season]
        # Get the final rank for the 2 previous seasons
        filename_previous1 = self.league + '_' + \
            SEASONS_INDEX[str(season_index - 1)] + '_final_ranking.csv'
        df = pd.read_csv(path_root + '/data/' + filename, sep=';')
        print df.head()
        try:
            f_rk_ps1_h = df.loc[self.hteam, 'Pos']
        except Exception as e:
            raise e

        try:
            f_rk_ps1_a = df.loc[self.ateam, 'Pos']
        except Exception as e:
            raise e

        filename_previous2 = self.league + '_' + \
            SEASONS_INDEX[str(season_index - 2)] + '_final_ranking.csv'
        df = pd.read_csv(path_root + '/data/' + filename, sep=';')
        print df.head()
        try:
            f_rk_ps2_h = df.loc[self.hteam, 'Pos']
        except Exception as e:
            raise e

        try:
            f_rk_ps2_a = df.loc[self.ateam, 'Pos']
        except Exception as e:
            raise e

        return [f_rk_ps1_h, f_rk_ps1_a, f_rk_ps2_h, f_rk_ps2_a]

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

if __name__ == '__main__':

    game = Game()
    today = dt.date.today()
    game(['AS Monaco', 'Olympique de Marseille'], '2013_2014', 'F1', dt.date(2013, 8, 9))
    print game._get_final_rank_previous_season()
