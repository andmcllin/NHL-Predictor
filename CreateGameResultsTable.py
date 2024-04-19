from ScheduleAndScoresPull import getPastScheduleAndScores
from TeamStatsPull import getTeamStats
import pandas as pd
import numpy as np

def createGameResultsCSV(startyear, endyear):
    years = np.arange(startyear, endyear, 1)

    df = pd.DataFrame()

    for year in years:
        scores_df = getPastScheduleAndScores(year)

        scores_df['Date'] = pd.to_datetime(scores_df['Date'])
        scores_df.rename(columns={'Visitor' : 'Visiting Team', 'Home' : 'Home Team'}, inplace=True)        
        scores_df['Home Win'] = np.where((scores_df['G.1'] >scores_df['G']), 1, 0)
        scores_df.insert(1, "Season", year)
        scores_df.insert(6, "Margin", scores_df['G.1'] - scores_df['G'])
        scores_df.insert(8, "Home Back to Back", False)
        scores_df.insert(9, "Visiting Back to Back", False)
        scores_df.drop(columns=['G', 'G.1'], inplace=True)

        teamstats_df = getTeamStats(year)

        statscolumns = teamstats_df.select_dtypes(include=[np.number]).drop(columns='Year').columns

        merged_df = pd.merge(scores_df, teamstats_df, left_on='Home Team', right_on='Team')
        merged_df = pd.merge(merged_df, teamstats_df, left_on='Visiting Team', right_on='Team', suffixes=('Home', 'Visitor'))

        del scores_df, teamstats_df

        for col in statscolumns:
            merged_df[col + 'Diff'] = merged_df[col + 'Home'] - merged_df[col + 'Visitor']

        merged_df = merged_df[merged_df.columns.drop(list(merged_df.filter(regex='Home$')))]
        merged_df = merged_df[merged_df.columns.drop(list(merged_df.filter(regex='Visitor$')))]

        df = pd.concat([df, merged_df]).reset_index(drop=True)

    team_list = np.unique(df['Home Team'])

    for team in team_list:
        temp_df = df[df['Home Team'].str.contains(team) | df['Visiting Team'].str.contains(team)]
        temp_df = temp_df.sort_values(by='Date', ascending=True)
        temp_df['Home Back to Back'] = np.where((temp_df['Date'].diff() == '1 days') & (temp_df['Home Team'] == team), True, False)
        temp_df['Visiting Back to Back'] = np.where((temp_df['Date'].diff() == '1 days') & (temp_df['Visiting Team'] == team), True, False)
        df.update(temp_df)
        
    del merged_df, temp_df, team_list

    df.to_csv('nhlGameResults.csv.gz', compression={'method':'gzip'}, index=False)