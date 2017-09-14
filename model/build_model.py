import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)

from modules import game as g
from modules import ranking as rk
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from pickle import dump, load
import matplotlib.pyplot as plt

from modules.helper import get_games_in_season

SAVE_FEATURES_OUTCOMES = True
UNPACK_FEATURES_OUTCOMES = False
LEARN = True

if __name__ == '__main__':

    # List of seasons used to build the model
    # SEASONS = ['2013_2014', '2014_2015']
    SEASONS = ['2016_2017']
    LEAGUE = 'E0'
    MODEL_VERSION = '_' + SEASONS[0] + '_' + 'correction'

    # Construct the features/outcomes
    features = []
    outcomes = []

    league = LEAGUE
    if UNPACK_FEATURES_OUTCOMES:
        features_pkl = open(
            basedir + '/stored_features/features_' + LEAGUE + '_' + SEASONS[0] + '.pkl', "r")  # Pickling
        features = load(features_pkl)
        outcomes_pkl = open(
            basedir + '/stored_features/outcomes_' + LEAGUE + '_' + SEASONS[0] + '.pkl', "r")  # Pickling
        outcomes = load(outcomes_pkl)
    else:
        for season in SEASONS:
            games_in_season, dates_dt = get_games_in_season(season, league)
            for game, date_dt in list(zip(games_in_season, dates_dt)):
                try:
                    game_inst = g.Game()
                    game_inst(game, season, league, date_dt)
                    features.append(game_inst.features)
                    outcomes.append(game_inst.outcome[0])
                except Exception as e:
                    print e
                    print 'Ranking is None'

    if SAVE_FEATURES_OUTCOMES:
        features_pkl = open(
            basedir + '/stored_features/features_' + LEAGUE + '_' + SEASONS[0] + '.pkl', "wb")  # Pickling
        dump(features, features_pkl)
        features_pkl.close()
        outcomes_pkl = open(
            basedir + '/stored_features/outcomes_' + LEAGUE + '_' + SEASONS[0] + '.pkl', "wb")  # Pickling
        dump(outcomes, outcomes_pkl)
        outcomes_pkl.close()
        # features.to_pickle(basedir + '/stored_features/features.p')

    # features and outcomes can now feed/train the model
    # print outcomes
    # Normalization step
    # Standardization issues??? need to pickle the standardizer???
    # features_normalized = normalize(features)
    features_normalized = features

    # Launch training
    if LEARN:
        learner = LinearSVC()
        learner.fit(features_normalized, outcomes)
        out_file = open(basedir + '/stored_models/linearSVC_' +
                        LEAGUE + '_' + MODEL_VERSION + '.pkl', 'wb')
        dump(learner, out_file)
        out_file.close()
    else:
        out_file = open(basedir + '/stored_models/linearSVC_' +
                        LEAGUE + '_' + MODEL_VERSION + '.pkl', 'rb')
        learner = load(out_file)

    # Training score
    print learner.score(features_normalized, outcomes)
    predicted = learner.predict(features_normalized)
    print confusion_matrix(outcomes, predicted)
    print roc_auc_score(outcomes, learner.decision_function(features_normalized))
    fpr, tpr, thresholds = roc_curve(
        outcomes, learner.decision_function(features_normalized))
    os.system('say "Almost Finished"')
    plt.figure()
    plt.plot(fpr, tpr)
    plt.show()
    os.system('say "Finished"')
