import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)

from modules import game as g
from modules import ranking as rk
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import cross_val_predict
from pickle import dump, load
import matplotlib.pyplot as plt

from modules.helper import get_games_in_season

SAVE_FEATURES_OUTCOMES = False
UNPACK_FEATURES_OUTCOMES = True
LEARN = False
PICKLE_STANDARDIZER = True

if __name__ == '__main__':

    # List of seasons used to build the model
    # SEASONS = ['2013_2014', '2014_2015']
    SEASONS = ['2016_2017']
    LEAGUE = 'E0'
    MODEL_VERSION = '_' + SEASONS[0]

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
                game_inst = g.Game()
                game_inst(game, season, league, date_dt)
                if not(len(np.unique(game_inst.features[4:9])) == 1):
                    features.append(game_inst.features)
                    outcomes.append(game_inst.outcome[0])

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
    if PICKLE_STANDARDIZER:
        scaler = StandardScaler()
        scaler.fit(features)
        features_standardized = scaler.transform(features)
        features_normalized = features_standardized
        out_file = open(basedir + '/stored_standardizers/standard_' +
                        LEAGUE + '_' + MODEL_VERSION + '.pkl', 'wb')
        dump(scaler, out_file)
        out_file.close()
    else:
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
    # os.system('say "Finished"')

    # Cross-validation
    cv_learner = LinearSVC()
    cv_predictions = cross_val_predict(
        cv_learner, features_normalized, outcomes, cv=3)
    print cv_predictions