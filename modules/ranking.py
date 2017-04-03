import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)
import pandas as pd
import datetime as dt
from constants import CURRENT_SEASON


class Ranking(object):

    def __init__(self):
        """
        ...
        """
        self.season = None
        self.league = None
        self.date_dt = None
        self.week_nb = None
        self.table = None

    def __call__(self, season, league, date_dt):

        self.season = season
        self.league = league
        self.date_dt = date_dt
        self.week_nb = self._get_previous_week_nb_from_date()
        self.table = self._get_table()

    def _get_table(self):

        if self.date_dt is None:
            # We retrieve the final rankings of the season
            filename = self.league + '_' + self.season + '_final_ranking.csv'
            df = pd.read_csv(path_root + '/data/' + filename, sep=';')
        else:
            # Need to draw the ranking as it is in current season or as it was
            # in previous season
            # Get the week/round number out of the date...
            week_nb = self.week_nb
            filename = self.league + '_' + self.season + \
                '_' + 'ranking_w' + str(week_nb) + '.csv'
            df = pd.read_csv(path_root + '/data/' + filename, sep=',')
        # ['Pos' 'Team' 'Pld' 'W' 'D' 'L' 'GF' 'GA' 'GD' 'Pts']
        list_col = df.columns.values
        df.index = df['Team']
        df = df.drop(['Team'],1)
        if 'Qualification or relegation' in list_col:
            df = df.drop(['Qualification or relegation'], 1)

        print df.head()
        return df

    def _get_empty_table(self):
        return {}

    def _complete_table(self, empty_table):
        table = empty_table
        return table

    def _get_previous_week_nb_from_date(self):

        filename = self.league + '_' + self.season + '_dates.csv'
        df = pd.read_csv(path_root + '/data/' + filename, sep=';')
        dd = df.copy()
        print dd.dtypes
        # dd['start_date'] = dd['start_date'].apply(lambda x: dt.date(x))
        dd['start_date'] = dd['start_date'].apply(
            lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date())
        # dd.index = dd['week_nb']
        dd = dd[dd['start_date'] > self.date_dt]
        return dd.iloc[0]['week_nb']

if __name__ == '__main__':

    ranking = Ranking()
    ranking('2013_2014', 'F1', dt.date(2013, 12, 1))
    df = ranking.table
    print df.loc['AS Monaco', 'Pos']
