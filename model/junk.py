import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)

from modules import game as g
from modules import ranking as rk
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from pickle import dump, load
import matplotlib.pyplot as plt

from modules.helper import get_games_in_season

SAVE_FEATURES_OUTCOMES = False
UNPACK_FEATURES_OUTCOMES = True
LEARN = False

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
        print 'else'

    features_labels = ['rank_h', 'rank_a', 'points_h', 'points_a', 'outcome_h_1', 'outcome_h_2',
                   'outcome_h_3', 'outcome_h_4', 'outcome_h_5', 'outcome_a_1', 'outcome_a_2',
                   'outcome_a_3', 'outcome_a_4', 'outcome_a_5', 'won_h', 'won_a', 'draw_h',
                   'draw_a', 'lost_h', 'lost_a', 'goalsdiff_h', 'goalsdiff_a', 'goalsfor_h',
                   'goalsfor_a', 'goalsagainst_h', 'goalsagainst_a']
    # print features
    df = pd.DataFrame.from_records(features, columns=features_labels)
    df['outcomes'] = outcomes
    # print df.head()
    print df.outcomes.describe()
    print df.outcomes.sum()
    