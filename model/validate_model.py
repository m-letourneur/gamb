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
from sklearn.metrics import confusion_matrix, classification_report
from pickle import load

UNPACK_FEATURES_OUTCOMES = False

if __name__ == '__main__':

    # List of seasons used to build the model
    SEASONS = ['2017_2018']
    LEAGUE = 'E0'

    # Construct the features/outcomes
    # features = pd.DataFrame()
    # outcomes = pd.Series()
    features = []
    outcomes = []

    if UNPACK_FEATURES_OUTCOMES:
        features_pkl = open(
            basedir + '/stored_features/features.pkl', "r")  # Pickling
        features = load(features_pkl)
        outcomes_pkl = open(
            basedir + '/stored_features/outcomes.pkl', "r")  # Pickling
        outcomes = load(outcomes_pkl)
        # features = pd.read_pickle(basedir + '/stored_features/features.p')
    else:
        league = LEAGUE
        for season in SEASONS:
            games_in_season, dates_dt = get_games_in_season(season, league)
            for game, date_dt in list(zip(games_in_season, dates_dt)):
                game_inst = g.Game()
                game_inst(game, season, league, date_dt)
                features.append(game_inst.features)
                outcomes.append(game_inst.outcome[0])
                # print 'in'

    # features and outcomes can now feed/train the model

    # Normalization step
    # Standardization issues??? need to pickle the standardizer???
    # features_normalized = normalize(features)
    features_normalized = features
    # Predicting using model
    p_file = open(basedir + '/stored_models/linearSVC_' +
                  LEAGUE + '.pkl', 'rb')
    model = load(p_file)
    predicted = model.predict(features_normalized)
    print 'predicted = ' + str(predicted)
    print '\noutcomes = ' + str(outcomes) + '\n'
    # Validation score
    print model.score(features_normalized, outcomes)
    print confusion_matrix(outcomes, predicted)
    print classification_report(outcomes, predicted, labels=['0','1'], target_names=['DL', 'W'])
