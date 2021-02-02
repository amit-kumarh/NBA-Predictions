import pandas as pd
import numpy as np

nbaSeasons = ['2020']
months = ['october', 'november', 'december', 'january', 'february', 'march', 'july', 'august']

for season in nbaSeasons:
    for month in months:
        matchups = pd.read_csv(f'./matchups/{month}{season}.csv')
        stats = pd.read_csv(f'./stats/{month}{season}.csv')

        stats['TEAM'].replace("LA Clippers", "Los Angeles Clippers", inplace=True)

        # Adding a new binary columns for Team 1 Win or Loss
        conditions = [
            matchups['1pts'] > matchups['2pts'],
            matchups['1pts'] < matchups['2pts']
        ]

        choices=[1,0]

        matchups['Team1Win'] = np.select(conditions, choices, 1)

        # Mergings the results and stats datasets, adding a prefix depending on which teams stats are being used
        df = matchups.merge(stats.add_prefix('Team1'), how='left', left_on=['Team1'], 
                           right_on=['Team1TEAM']).drop(['Team1TEAM'],
                                                        axis=1).merge(stats.add_prefix('Team2'), 
                                                                                    how='left', left_on=['Team2'], 
                                                                                    right_on=['Team2TEAM']).drop(['Team2TEAM'],axis=1)
        df.to_csv('final.csv', mode='a', index = False, header=True)
