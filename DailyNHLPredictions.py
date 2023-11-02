from ScheduleAndScoresPull import getTodaysSchedule
from TeamStatsPull import getTeamStats
import numpy as np
import pandas as pd
from keras.models import load_model

def makePredictions(date):
    schedule_df = getTodaysSchedule(date)

    schedule_df.rename(columns={'Visitor' : 'Visiting Team', 'Home' : 'Home Team'}, inplace=True)        
    schedule_df.drop(columns=['G', 'G.1'], inplace = True)

    if int(date.strftime("%m")) >= 9:
        year = int(date.strftime("%Y")) + 1
    else:
        year = int(date.strftime("%Y")) 

    stats_df = getTeamStats(year)

    statscolumns = stats_df.select_dtypes(include=[np.number]).drop(columns='Year').columns

    df = pd.merge(schedule_df, stats_df, left_on='Home Team', right_on='Team')
    df = pd.merge(df, stats_df, left_on='Visiting Team', right_on='Team', suffixes=('Home', 'Visitor'))

    del year, schedule_df, stats_df

    for col in statscolumns:
            df[col + 'Diff'] = df[col + 'Home'] - df[col + 'Visitor']

    df = df[df.columns.drop(list(df.filter(regex='Home$')))]
    df = df[df.columns.drop(list(df.filter(regex='Visitor$')))]
    df.set_index(['Date', 'Visiting Team', 'Home Team'], inplace=True)
    
    model = load_model('NHLPredictor.h5')

    predictions = pd.DataFrame(data=model.predict(df), columns=['Prediction'])

    del model

    df.reset_index(inplace=True)
    df = df[['Home Team', 'Visiting Team']]

    df = pd.concat([df, predictions], axis=1)

    del predictions

    for index in range(len(df)):
        winProb = df.loc[index, 'Prediction']
        winProb = round((winProb * 100), 2)
        homeTeam = df.loc[index, 'Home Team']
        awayTeam = df.loc[index, 'Visiting Team']

        if winProb >= 50:
            moneyline = (int(np.round(-((100 * winProb) / (winProb - 100)), 0)))
            moneyline = "-" + str(moneyline)
        else:
            moneyline = (int(np.round(-((100 * (winProb - 100)) / (winProb)), 0)))
            moneyline = "+" + str(moneyline)

        winProb = str(winProb)

        print('There is a ' + winProb + '%' + ' chance that the ' + homeTeam + ' will defeat the ' + awayTeam + '. ' + homeTeam + ': ' + moneyline)

    del df, winProb, homeTeam, awayTeam