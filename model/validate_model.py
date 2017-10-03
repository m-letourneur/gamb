import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)

from modules import game as g
from modules.helper import get_games_in_season, odd_score
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, roc_curve
from pickle import load
import matplotlib.pyplot as plt

UNPACK_FEATURES_OUTCOMES = False
PICKLE_STANDARDIZER = True

if __name__ == '__main__':

    # Season & league to validate the model on
    SEASONS = ['2017_2018']
    LEAGUE = 'E0'
    MODEL_VERSION = '_' + '2016_2017'  # Model to unpack
    # Construct the features/outcomes of the validation set
    features = []
    outcomes = []
    odd_h = []

    if UNPACK_FEATURES_OUTCOMES:
        features_pkl = open(
            basedir + '/stored_features/features_' + LEAGUE + '_' + SEASONS[0] + '.pkl', "r")  # Pickling
        features = load(features_pkl)
        outcomes_pkl = open(
            basedir + '/stored_features/outcomes_' + LEAGUE + '_' + SEASONS[0] + '.pkl', "r")  # Pickling
        outcomes = load(outcomes_pkl)
    else:
        league = LEAGUE
        for season in SEASONS:
            games_in_season, dates_dt = get_games_in_season(season, league)
            for game, date_dt in list(zip(games_in_season, dates_dt)):
                game_inst = g.Game()
                game_inst(game, season, league, date_dt)
                features.append(game_inst.features)
                outcomes.append(game_inst.outcome[0])
                odd_h.append(game_inst.odd_h)

    # features and outcomes can now feed/train the model
    # Normalization step
    if PICKLE_STANDARDIZER:
        scaler = StandardScaler()
        scaler.fit(features)
        features_standardized = scaler.transform(features)
        features_normalized = features_standardized
        out_file = open(basedir + '/stored_standardizers/standard_' +
                        LEAGUE + '_' + MODEL_VERSION + '.pkl', 'rb')
        scaler = load(out_file)
    else:
        features_normalized = features

    # Predicting using model
    p_file = open(basedir + '/stored_models/linearSVC_' +
                  LEAGUE + '_' + MODEL_VERSION + '.pkl', 'rb')
    model = load(p_file)
    predicted = model.predict(features_normalized)
    print 'predicted = ' + str(predicted)
    print '\noutcomes = ' + str(outcomes) + '\n'

    # Validation score
    predicted = model.predict(features_normalized)
    perf_file = open(basedir + '/stored_models/perf_linearSVC_' +
                     LEAGUE + '_' + MODEL_VERSION + '.txt', 'a')
    perf_file.write("\n--- Validation set ---\n\n")
    perf_file.write("Accuracy = "
                    + str(model.score(features_normalized, outcomes))
                    + "\n")
    perf_file.write("AUROC = "
                    + str(roc_auc_score(outcomes,
                                        model.decision_function(features_normalized)))
                    + "\n")
    perf_file.write("Confusion matrix = "
                    + str(confusion_matrix(outcomes, predicted))
                    + "\n\n")
    perf_file.close()

    print model.score(features_normalized, outcomes)
    print model.decision_function(features_normalized)
    print roc_auc_score(outcomes, model.decision_function(features_normalized))
    fpr, tpr, thresholds = roc_curve(
        outcomes, model.decision_function(features_normalized))
    # os.system('say "Almost Finished"')
    # plt.figure()
    # plt.plot(fpr, tpr)
    # plt.show()
    print confusion_matrix(outcomes, predicted)
    print classification_report(outcomes, predicted, labels=['0', '1'],
                                target_names=['DL', 'W'])

    print odd_h
    print np.sum(np.multiply(outcomes,odd_h))
    print np.sum(np.multiply(predicted,odd_h))
    print np.sum(outcomes)
    print np.sum(predicted)

    print('odd score = ' + str(odd_score(outcomes, predicted, odd_h)))

    os.system('say "Finished"')
