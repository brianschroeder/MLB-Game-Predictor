# Author
    # Brian Schroeder

# Synopsis
    # This program gets the winner for each game and outputs the stats they were leading in.
    # The Output will be the total number of times that category was higher for the winning team vs the losing

import requests
import json
from collections import Counter
import pandas as pd

winningStat = []

def mlb_games(gamedate):

    request = requests.get(f"http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={gamedate}").text
    request_json = json.loads(request)
    games = (request_json['dates'][0]['games'])

    for game in games:

        request = requests.get(f"http://statsapi.mlb.com{(game['link'])}").text
        request_json = json.loads(request)
        awayStats = (request_json['liveData']['boxscore']['teams']['away']['teamStats']['batting'])
        homeStats = (request_json['liveData']['boxscore']['teams']['home']['teamStats']['batting'])

        try:
            if (game['teams']['home']['isWinner']) == True:
                for key in homeStats.keys():
                    if homeStats[key] > awayStats[key]:
                        winningStat.append(key)
            else:
                for key in homeStats.keys():
                    if homeStats[key] < awayStats[key]:
                        winningStat.append(key)

        except:
            continue

mlb_games('04/01/2021')

common_winning_stats = (dict(Counter(winningStat)))
sorted_common_winning_stats = (sorted(common_winning_stats.items(), key=lambda x: x[1], reverse=True))

stats_dataframe = pd.DataFrame(data=sorted_common_winning_stats)

print(stats_dataframe)
