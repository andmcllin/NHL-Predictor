import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from io import StringIO


def getPastScheduleAndScores(year):
    time.sleep(3)

    base_url = 'https://www.hockey-reference.com/leagues/NHL_{}_games.html'
    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.find('table', {'id': 'games'})

    del base_url, req_url, data, soup

    if table is not None:

        df = pd.read_html(StringIO(str(table)))[0]

        del df['Att.'], df['LOG'], df['Notes']

        if 'Start (ET)' in df.columns :
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns :
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns :
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns :
            del df['Unnamed: 7']
            
        return df.dropna()

def getTodaysSchedule(date):   
    time.sleep(3)

    yearstring = date.strftime("%Y")

    if int(date.strftime("%m")) >= 9:
        year = int(yearstring) + 1
    else:
        year = int(yearstring)

    base_url = 'https://www.hockey-reference.com/leagues/NHL_{}_games.html'
    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.find('table', {'id': 'games'})

    del yearstring, year, base_url, req_url, data, soup

    if table is not None:

        df = pd.read_html(StringIO(str(table)))[0]

        del df['Att.'], df['LOG'], df['Notes']

        if 'Start (ET)' in df.columns:
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns:
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns:
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns:
            del df['Unnamed: 7']

        df = df.loc[df['Date'] == str(date)]

        return df