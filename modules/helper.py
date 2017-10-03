import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)
import pandas as pd
import datetime as dt
import numpy as np


def get_games_in_season(season, league):
    """
    List of games and associated list of dates in datetime format
    """
    filename = league + '_' + season + '.csv'
    df = pd.read_csv(path_root + '/data/' + filename)
    df = df.dropna()

    games_in_season = df.copy()
    dates_dt = df.copy()
    games_in_season = games_in_season[['HomeTeam', 'AwayTeam']]
    dates_dt = dates_dt['Date'].apply(
        lambda x: dt.datetime.strptime(str(x), '%d/%m/%y').date())
    # dates_dt['Date'] = dates_dt['Date'].apply(
    # lambda x: dt.datetime.strptime(str(x), '%d/%m/%y').date())

    games_in_season = games_in_season.values.tolist()
    dates_dt = (dates_dt.values).tolist()

    return games_in_season, dates_dt


def get_games_next_week(season, league):
    current_dt = dt.date.today()
    # Identify the next week nb based on current date
    # Need to scrap... But not essential here
    week_nb = 0
    return []


def get_outcome_from_file(h_team, a_team, season, league):
    filename = league + '_' + season + '.csv'
    df = pd.read_csv(path_root + '/data/' + filename)
    df = df.dropna()
    df = df[['HomeTeam', 'AwayTeam', 'FTR']]
    df = df[df['HomeTeam'] == h_team]
    df = df[df['AwayTeam'] == a_team]
    return map(lambda x: binarize_outcome(x), df['FTR'].values[0])


def get_odd_from_file(h_team, a_team, season, league):
    filename = league + '_' + season + '.csv'
    df = pd.read_csv(path_root + '/data/' + filename)
    df = df.dropna()
    df = df[['HomeTeam', 'AwayTeam', 'B365H']]
    df = df[df['HomeTeam'] == h_team]
    df = df[df['AwayTeam'] == a_team]
    return df['B365H'].values[0]


def odd_score(outcomes, predicted, odd_h):
    yyodd = np.multiply(np.multiply(outcomes, predicted), odd_h)
    yy = np.multiply(outcomes, np.ones(len(predicted)) - predicted)
    return (np.sum(yyodd - yy) - np.sum(predicted))


def binarize_outcome(s):
    # The target variable is set to be the win of the Home Team
    if s == 'W' or s == 'H':
        return 1
    else:
        return 0


def get_week_nb_from_date(season, league, date):
    # Convert the date into the past associated week number for the season,
    # league
    return 0

if __name__ == '__main__':

    # games_in_season, dates_dt = get_games_in_season('2013_2014', 'F1')
    # print games_in_season, dates_dt
    print get_outcome_from_file('Bordeaux', 'Paris SG', '2012_2013', 'F1')
    print get_games_in_season('2012_2013', 'F1')
    print get_odd_from_file('Bordeaux', 'Paris SG', '2012_2013', 'F1')
