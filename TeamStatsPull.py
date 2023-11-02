import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
from io import StringIO
import time
from sklearn.preprocessing import StandardScaler

def getTeamStats(year):
    base_url = 'https://www.hockey-reference.com/leagues/NHL_{}.html'
    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.select_one('h2:-soup-contains("Team Analytics (5-on-5)")').find_next(text=lambda t: isinstance(t, Comment))

    soup = BeautifulSoup(str(table), 'html.parser')
    table = soup.find('table', attrs={'id': 'stats_adv'})
    df = pd.read_html(StringIO(str(table)))[0]

    del base_url, req_url, data, soup, table

    columnlist = list()

    for index in df.columns:
        columnlist.append(index[1])

    df = pd.DataFrame(df.values, columns=columnlist)
    df = df.rename(columns={'Unnamed: 1_level_1':'Team'})

    time.sleep(3)

    df['Year'] = year
    df.set_index(['Team', 'Year'], inplace=True)
    df.drop(columns=['Rk'], inplace=True)

    scaler = StandardScaler()

    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    df.reset_index(inplace=True)
   
    return df