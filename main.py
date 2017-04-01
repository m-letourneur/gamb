import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
print basedir
print os.path.realpath(__file__)
import datetime as dt

# import classes
sys.path.insert(1, basedir + '/modules')
from modules import game as g
from sklearn.svm import LinearSVC
from modules.helper import get_games_next_week

if __name__ == '__main__':

    # At a given date in time
    today_dt = dt.date.today()
    CURRENT_DATE = today_dt
    # Choose the league to work on
    LEAGUE = 'F1'
    # Season to work on
    SEASON = '2016_2017'
    # Input: list of next games // or Week number and retrieve the list of
    # games
    NEXT_WEEK_GAMES = [['Bastia', 'Lille'], ['Nice', 'Bordeaux']]
    
    features = []
    outcomes = []
    # For each game, predict whether the Home Team is gonna win
    for game in NEXT_WEEK_GAMES:
        game_inst = g.Game()
        game_inst(game, SEASON, LEAGUE, CURRENT_DATE)
        features.append(game_inst.features)
        outcomes.append(game_inst.outcome)
    

    features_normalized = normalize(features)
    # Predicting using model
    p_file = open(basedir + '/stored_models/linearSVC_' + LEAGUE + '.p', 'wr')
    model = load(p_file)
    predicted = model.fit(features_normalized)
    decision_function = model.decision_function(features_normalized)
    
    print "Probability and comparison to the odds"
