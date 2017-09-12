import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)

from modules import game as g
from modules.helper import get_games_in_season
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from pickle import load


# def _get_games_in_season(season, league):
#     """
#     List of games and associated list of dates in datetime format
#     """
#     games_in_season, dates_dt = [], []

#     return games_in_season, dates_dt

if __name__ == '__main__':

    # List of seasons used to build the model
    SEASONS = ['2016_2017']
    LEAGUE = 'E0'

    # Construct the features/outcomes
    # features = pd.DataFrame()
    # outcomes = pd.Series()
    features = []
    outcomes = []

    league = LEAGUE
    for season in SEASONS:
        games_in_season, dates_dt = get_games_in_season(season, league)
        for game, date_dt in zip(games_in_season, dates_dt):
            game_inst = g.Game()
            game_inst(game, season, league, date_dt)
            features.append(game_inst.features)
            outcomes.append(game_inst.outcome)

    # features and outcomes can now feed/train the model

    # Normalization step
    # Standardization issues??? need to pickle the standardizer???
    # features_normalized = normalize(features)
    features_normalized = features
    # Predicting using model
    p_file = open(basedir + '/stored_models/linearSVC_' +
                  LEAGUE + '.p', 'rb')
    model = load(p_file)
    predicted = model.fit(features_normalized)

    # Validation score
    print confusion_matrix(outcomes, predicted)
