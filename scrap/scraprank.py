from bs4 import BeautifulSoup
from urllib import urlopen

season = '2016_2017' 
teams_in_season = ['Manchester United']

# for week in range(1,39):
for week in [1]:
    url = 'https://www.premierleague.com/tables?co=1&se=54&mw=1-' + \
        str(week) + '&ha=-1'
    html = urlopen(url).read()
    # print html
    sp = BeautifulSoup(html, "html.parser")
    # print sp
    # print sp.find_agll('td')
    # for tr in sp.find_all('tr')[1::]:
    # 	print tr
    # 	print tr
    tbody = sp.find_all('tbody')
    # print tbody
    for team in teams_in_season:
         tr = tbody.find_all(team)

    # print sp
# print sp

print "done"
