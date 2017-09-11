import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)
import pandas as pd
import datetime as dt


class Ranking(object):

    def __init__(self):
        """
        Table template:
            {
                "Bastia" : 14
            }
        """
        self.season = None
        self.league = None
        self.date_dt = None
        self.table = None

    def __call__(self, season, league, date_dt):

        self.season = season
        self.league = league
        self.date_dt = date_dt
        self.table = self._get_table()

    def _get_empty_table(self):
        table = {}
        teams = self._get_teams_in_season()
        # print teams
        for team in teams:
            table[team] = {
                'points': 0,
                'position': 0,
                'won': 0,
                'lost': 0,
                'draw': 0,
                'goalsfor': 0,
                'goalsagainst': 0,
                'goalsdiff': 0,
                'former': [],
                'played': 0
            }
        self.table = table

    def _get_teams_in_season(self):
        filename = self.league + '_' + self.season + '.csv'
        # e = "Div,Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR,HTHG,HTAG,HTR"
        df = pd.read_csv(path_root + '/data/' + filename)
        return list(df.loc[:, 'HomeTeam'].unique())

    def _get_table(self):
        filename = self.league + '_' + self.season + '.csv'
        df = pd.read_csv(path_root + '/data/' + filename)
        self._get_empty_table()
        # print self.table
        table = None
        for ind in df.index:
            date_g = dt.datetime.strptime(
                df.loc[ind, 'Date'], '%d/%m/%y').date()
            if date_g > self.date_dt:
                print 'out'
                break
            else:
                # print 'in'
                self._update_table(df.iloc[ind])
                # print self.table
                table = self.table

        return table

    def _update_table(self, game):
        self._update_points(game)
        self._update_played(game)
        self._update_goals(game)
        self._update_positions()
        # print self.table

    def _update_points(self, game):
        hteam = game['HomeTeam']
        ateam = game['AwayTeam']

        if len(self.table[hteam]['former']) == 5:
            self.table[hteam]['former'] = self.table[hteam]['former'][1:5]
        if len(self.table[ateam]['former']) == 5:
            self.table[ateam]['former'] = self.table[ateam]['former'][1:5]

        if game['FTR'] == 'H':
            self.table[hteam]['points'] += 3
            self.table[hteam]['won'] += 1
            self.table[ateam]['lost'] += 1
            self.table[hteam]['former'].append('W')
            self.table[ateam]['former'].append('L')
        elif game['FTR'] == 'A':
            self.table[ateam]['points'] += 3
            self.table[hteam]['lost'] += 1
            self.table[ateam]['won'] += 1
            self.table[hteam]['former'].append('L')
            self.table[ateam]['former'].append('W')
        else:
            self.table[hteam]['points'] += 1
            self.table[ateam]['points'] += 1
            self.table[hteam]['draw'] += 1
            self.table[ateam]['draw'] += 1
            self.table[hteam]['former'].append('D')
            self.table[ateam]['former'].append('D')

    def _update_played(self, game):
        hteam = game['HomeTeam']
        ateam = game['AwayTeam']
        self.table[hteam]['played'] += 1
        self.table[ateam]['played'] += 1

    def _update_goals(self, game):
        hteam = game['HomeTeam']
        ateam = game['AwayTeam']
        self.table[hteam]['goalsfor'] += game['FTHG']
        self.table[ateam]['goalsfor'] += game['FTAG']
        self.table[hteam]['goalsagainst'] += game['FTAG']
        self.table[ateam]['goalsagainst'] += game['FTHG']
        self.table[hteam]['goalsdiff'] = self.table[
            hteam]['goalsfor'] - self.table[hteam]['goalsagainst']
        self.table[ateam]['goalsdiff'] = self.table[
            ateam]['goalsfor'] - self.table[ateam]['goalsagainst']

    def _update_positions(self):
        # Sort everything out
        # print 'update pos'
        list_2_sort = []
        for team in self.table.keys():
            list_2_sort.append([team, self.table[team]['points'], self.table[
                               team]['goalsdiff'], self.table[team]['goalsfor']])

        sorted_list = sorted(list_2_sort, key=lambda x: (-x[1], -x[2], -x[3]))
        # print sorted_list
        for ind in range(len(sorted_list)):
            team = sorted_list[ind][0]
            self.table[team]['position'] = ind + 1

if __name__ == '__main__':
    season = '2016_2017'
    league = 'E0'
    date_dt = dt.date(year=2017, month=7, day=31)
    rank_ = Ranking()
    # print "output"
    # print rank_.season
    rank_(season, league, date_dt)
    print rank_.table
