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
    table = soup.select_one('h2:-soup-contains("Team Analytics (5-on-5)")').find_next(string=lambda t: isinstance(t, Comment))

    new_soup = BeautifulSoup(str(table), 'html.parser')
    table = new_soup.find('table', attrs={'id': 'stats_adv'})
    adv_df = pd.read_html(StringIO(str(table)))[0]

    del table, new_soup

    time.sleep(3)

    columnlist = list()

    for index in adv_df.columns:
        columnlist.append(index[1])

    adv_df = pd.DataFrame(adv_df.values, columns=columnlist)
    adv_df = adv_df.rename(columns={'Unnamed: 1_level_1':'Team'})
    adv_df['Year'] = year
    adv_df['Team'] = adv_df['Team'].str.replace('\*', '', regex=True)
    adv_df.set_index(['Team', 'Year'], inplace=True)
    adv_df.drop(columns=['Rk'], inplace=True)    

    table = soup.select_one('h2:-soup-contains("Team Statistics")').find_next(string=lambda t: isinstance(t, Comment))

    new_soup = BeautifulSoup(str(table), 'html.parser')
    table = new_soup.find('table', attrs={'id': 'stats'})
    pp_df = pd.read_html(StringIO(str(table)))[0]

    time.sleep(3)

    del base_url, req_url, data, soup, table, new_soup

    pp_df = pp_df[['Unnamed: 1_level_0', 'Special Teams']]

    columnlist = list()

    for index in pp_df.columns:
        columnlist.append(index[1])

    pp_df = pd.DataFrame(pp_df.values, columns=columnlist)
    pp_df = pp_df.rename(columns={'Unnamed: 1_level_1':'Team'})
    pp_df['Year'] = year
    pp_df['Team'] = pp_df['Team'].str.replace('\*', '', regex=True)
    pp_df.set_index(['Team', 'Year'], inplace=True)

    df = pd.merge(adv_df, pp_df, on=['Team', 'Year'])

    del adv_df, pp_df

    scaler = StandardScaler()

    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    df.reset_index(inplace=True)
   
    return df