import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
path_root = os.path.dirname(basedir)
sys.path.insert(0, path_root)
import time

import urllib2
from bs4 import BeautifulSoup as bs
from constants import URL_INDEX_SEASON_F1
import pandas as pd
from selenium import webdriver


def scrap_date(season, league, week_nb):
    index_season = URL_INDEX_SEASON_F1[season]
    print index_season
    # 'http://www.lfp.fr/ligue1/calendrier_resultat#sai=100&jour=31'
    url = ('http://www.lfp.fr/ligue1/calendrier_resultat#sai=%s&jour=%s') % (
        str(index_season), str(week_nb))
    print url
    """
        <th class="hide" scope="col">Position</th>
        <th class="hide" scope="col">Evolution</th>
        <th scope="col" class="club">Team</th>
        <th scope="col"><abbr title="Played">Pld</abbr></th>
        <th scope="col"><abbr title="Wins">W</abbr></th>
        <th scope="col"><abbr title="Draws">D</abbr></th>
        <th scope="col"><abbr title="Loses">L</abbr></th>
        <th scope="col"><abbr title="For">F</abbr></th>
        <th scope="col"><abbr title="Against">A</abbr></th>
        <th scope="col"><abbr title="LIB_BUTS_DIFFERENCE">GD</abbr></th>
        <th scope="col"><abbr title="Points">Pts</abbr></th>

        df --> Pos;Team;Pld;W;D;L;GF;GA;GD;Pts;
    """
    # driver = webdriver.Safari()  # selenium for PhantomJS
    driver = webdriver.Chrome('/Users/Caco/Documents/WspacePython/chromedriver')
    driver.get(url)
    try:
        soup = bs(driver.page_source, 'html.parser')
    except Exception as e:
        raise e

    all_teams_stats = []
    previous_pos = 1
    trs = soup.find_all('tr')
    for tr_ind in range(len(trs)):
        tds = trs[tr_ind].find_all('td')
        try:
            team_stats = []
            for td_ind in [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                if td_ind == 0:
                    if tds[td_ind].text == '-':
                        team_stats.append(previous_pos)
                    else:
                        team_stats.append(int(tds[td_ind].text))
                        previous_pos = int(tds[td_ind].text)
                elif td_ind == 2:
                    str_ = tds[td_ind].text
                    str_ = str_.replace('\n', '').replace(
                        '\r', '').replace('\t', '').replace("  ", "")
                    team_stats.append(str_)
                else:
                    team_stats.append(int(tds[td_ind].text))
            all_teams_stats.append(team_stats)
        except Exception as e:
            print e
            pass

    df = pd.DataFrame(all_teams_stats, columns=['Pos', 'Team', 'Pld', 'W', 'D',
                                                'L', 'GF', 'GA', 'GD', 'Pts'])

    try:
        df.index = df['Team']
        df = df.drop(['Team'], 1)
        return df
    except Exception as e:
        print e
        pass
        return df


if __name__ == '__main__':

    start_time = time.time()

    # season = '2013_2014'
    # league = 'F1'
    # week_nb = 1
    # df = scrap_table(season, league, week_nb)
    # df.to_csv(path_root + '/data/' + league + '_' + season +
    #           '_' + 'ranking_w' + str(week_nb) + '.csv', encoding='utf-8')
    # print df

    # league = 'F1'
    # for season in ['2013_2014', '2016_2017']:
    #     for week_nb in range(1, 32):
    #         try:
    #             path_filename = (path_root + '/data/' + league + '_' +
    #                              season + '_' + 'ranking_w' + str(week_nb) + '.csv')
    #             if not(os.path.exists(path_filename)):
    #                 df = scrap_table(season, league, week_nb)
    #                 df.to_csv(path_root + '/data/' + league + '_' +
    #                           season + '_' + 'ranking_w' + str(week_nb) + '.csv', encoding='utf-8')
    #         except Exception as e:
    #             print path_filename
    #             print df
    #             raise e

    print("--- %s seconds ---" % (time.time() - start_time))
