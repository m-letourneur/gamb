import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)

from modules import game as g
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from pickle import dump, load

from modules.helper import get_games_in_season

SAVE_FEATURES_OUTCOMES = True
UNPACK_FEATURES_OUTCOMES = False

if __name__ == '__main__':

    # List of seasons used to build the model
    # SEASONS = ['2013_2014', '2014_2015']
    SEASONS = ['2016_2017']
    LEAGUE = 'E0'

    # Construct the features/outcomes
    # features = pd.DataFrame()
    # outcomes = pd.Series()
    features = []
    outcomes = []

    league = LEAGUE

    if UNPACK_FEATURES_OUTCOMES:
        features_pkl = open(
            basedir + '/stored_features/features.pkl', "r")  # Pickling
        features = load(features_pkl)
        outcomes_pkl = open(
            basedir + '/stored_features/outcomes.pkl', "r")  # Pickling
        outcomes = load(outcomes_pkl)
        # features = pd.read_pickle(basedir + '/stored_features/features.p')
    else:
        for season in SEASONS:
            games_in_season, dates_dt = get_games_in_season(season, league)
            for game, date_dt in list(zip(games_in_season, dates_dt)):
                game_inst = g.Game()
                game_inst(game, season, league, date_dt)
                features.append(game_inst.features)
                outcomes.append(game_inst.outcome[0])
                # print 'in'

    if SAVE_FEATURES_OUTCOMES:
        features_pkl = open(
            basedir + '/stored_features/features.pkl', "wb")  # Pickling
        dump(features, features_pkl)
        features_pkl.close()
        outcomes_pkl = open(
            basedir + '/stored_features/outcomes.pkl', "wb")  # Pickling
        dump(outcomes, outcomes_pkl)
        outcomes_pkl.close()
        # features.to_pickle(basedir + '/stored_features/features.p')

    # features and outcomes can now feed/train the model
    # print outcomes
    # Normalization step
    # Standardization issues??? need to pickle the standardizer???
    # features_normalized = normalize(features)
    features_normalized = features
    # print features_normalized

    # Launch training
    learner = LinearSVC()
    learner.fit(features_normalized, outcomes)
    out_file = open(basedir + '/stored_models/linearSVC_' +
                    LEAGUE + '.pkl', 'wb')
    dump(learner, out_file)
    out_file.close()

    # Training score
    print learner.score(features_normalized, outcomes)
    predicted = learner.predict(features_normalized)
    print confusion_matrix(outcomes, predicted)
    os.system('say "Finished"')
