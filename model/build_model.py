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
from pickle import dump

from modules.helper import get_games_in_season


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
    for season in SEASONS:
        games_in_season, dates_dt = get_games_in_season(season, league)
        print zip(games_in_season, dates_dt)
        for game, date_dt in zip(games_in_season, dates_dt):
            game_inst = g.Game()
            game_inst(game, season, league, date_dt)
            features.append(game_inst.features)
            outcomes.append(game_inst.outcome)
            print 'in'

    # features and outcomes can now feed/train the model

    # Normalization step
    # Standardization issues??? need to pickle the standardizer???
    # features_normalized = normalize(features)
    features_normalized = features
    print features_normalized

    # Launch training
    learner = LinearSVC()
    learner.fit(features_normalized, outcomes)
    out_file = open(basedir + '/stored_models/linearSVC_' +
                    LEAGUE + '.p', 'wr')
    dump(learner, out_file)

    # Training score
    learner.score(features_normalized, outcomes)
    predicted = learner.predict(features_normalized)
    print confusion_matrix(outcomes, predicted)
