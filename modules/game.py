import ranking as rk
import datetime as dt
from helper import get_outcome_from_file

features_labels = ['rank_h', 'rank_a', 'points_h', 'points_a', 'outcome_h_1', 'outcome_h_2',
                   'outcome_h_3', 'outcome_h_4', 'outcome_h_5', 'outcome_a_1', 'outcome_a_2',
                   'outcome_a_3', 'outcome_a_4', 'outcome_a_5', 'won_h', 'won_a', 'draw_h',
                   'draw_a', 'lost_h', 'lost_a', 'goalsdiff_h', 'goalsdiff_a', 'goalsfor_h',
                   'goalsfor_a', 'goalsagainst_h', 'goalsagainst_a']


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
        features.extend(self._get_points())
        features.extend(self._get_last_outcomes())
        features.extend(self._get_won())
        features.extend(self._get_draw())
        features.extend(self._get_lost())
        features.extend(self._get_goalsdiff())
        features.extend(self._get_goalsfor())
        features.extend(self._get_goalsagainst())

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
        current_ranking = rk.Ranking(self.season, self.league)
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        rank_h = current_ranking.table[self.hteam]['position']
        # Away team
        rank_a = current_ranking.table[self.ateam]['position']

        ranks = [rank_h, rank_a]
        return ranks

    def _get_points(self):
        # Get the current rank in the league for both teams
        current_ranking = rk.Ranking(self.season, self.league)
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        points_h = current_ranking.table[self.hteam]['points']
        # Away team
        points_a = current_ranking.table[self.ateam]['points']

        points = [points_h, points_a]
        return points

    def _get_last_outcomes(self):
        # Get the lastest outcomes for both teams
        current_ranking = rk.Ranking(self.season, self.league)
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        last_h = current_ranking.table[self.hteam]['former'][0:5]
        # Away team
        last_a = current_ranking.table[self.ateam]['former'][0:5]

        return map(lambda x: convert_outcome2int(x), last_h + last_a)

    def _get_won(self):
        # Get the nb of wins for both teams
        current_ranking = rk.Ranking(self.season, self.league)
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        last_h = current_ranking.table[self.hteam]['won']
        # Away team
        last_a = current_ranking.table[self.ateam]['won']

        return [last_h, last_a]

    def _get_draw(self):
        # Get the nb of draws for both teams
        current_ranking = rk.Ranking(self.season, self.league)
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        last_h = current_ranking.table[self.hteam]['draw']
        # Away team
        last_a = current_ranking.table[self.ateam]['draw']

        return [last_h, last_a]

    def _get_lost(self):
        # Get the lost games for both teams
        current_ranking = rk.Ranking(self.season, self.league)
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        last_h = current_ranking.table[self.hteam]['lost']
        # Away team
        last_a = current_ranking.table[self.ateam]['lost']

        return [last_h, last_a]

    def _get_goalsdiff(self):
        # Get the goals difference score for both teams
        current_ranking = rk.Ranking(self.season, self.league)
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        goalsdiff_h = current_ranking.table[self.hteam]['goalsdiff']
        # Away team
        goalsdiff_a = current_ranking.table[self.ateam]['goalsdiff']

        return [goalsdiff_h, goalsdiff_a]

    def _get_goalsfor(self):
        # Get the goals for score for both teams
        current_ranking = rk.Ranking(self.season, self.league)
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        goalsfor_h = current_ranking.table[self.hteam]['goalsfor']
        # Away team
        goalsfor_a = current_ranking.table[self.ateam]['goalsfor']

        return [goalsfor_h, goalsfor_a]

    def _get_goalsagainst(self):
        # Get the goals against score for both teams
        current_ranking = rk.Ranking(self.season, self.league)
        current_ranking(self.season, self.league, self.date_dt)
        # Home team
        goalsagainst_h = current_ranking.table[self.hteam]['goalsagainst']
        # Away team
        goalsagainst_a = current_ranking.table[self.ateam]['goalsagainst']

        return [goalsagainst_h, goalsagainst_a]

    def _get_nb_goals_scored_previous_game(self):
        # Get last game stats for both teams
        # goals or other stats...
        return []

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


def convert_outcome2int(s):
    if s == 'W' or s == 'H':
        return 1
    elif (s == 'D' or s == 'L' or s == 'A'):
        return 0
    else:
        # the game outcome is unknown (if P or -1)
        return -1

# def convert_outcome2bin(s):
#     if s == 'W' or s == 'H':
#         return 1
#     else:
#         return 0

if __name__ == '__main__':
    print map(lambda x: convert_outcome2int(x), ['H', 'A', 'D'])
    # print map(lambda x: convert_outcome2bin(x), ['H', 'A', 'D'])

    game = ['Leicester','Arsenal']
    season='2016_2017'
    league='E0'
    date_dt = dt.date(year=2016, month=8, day=20)
    game_inst = Game()
    game_inst(game, season, league, date_dt)
    print game_inst.features
    print len(game_inst.features) == 26
    import ranking as rk
    r = rk.Ranking(season, league)
    r(season, league, date_dt)
    # print r.table

