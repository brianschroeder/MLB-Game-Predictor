# Author
    # Brian Schroeder

# Synopsis
    # This program gets the winner for each game and outputs the stats they were leading in.
    # The Output will be the total number of Games that category was higher for the winning team vs the losing

import requests
import json
from collections import Counter
from prettytable import PrettyTable
import datetime

batting_winningStats = []
pitching_winningStats = []
categories = 'batting', 'pitching'

#Format for Dates: Day,Month,Year
startDate = "01-01-2019"
endDate = "31-12-2019"

# List of Stats that are better when lower

batting_stats_adjustment = "atBatsPerHomeRun", "caughtStealing", "flyOuts", "groundIntoDoublePlay", "groundIntoTriplePlay", "groundOuts", "leftOnBase", "strikeOuts"
pitching_stats_adjustment = "airOuts", "atBats", "balks", "baseOnBalls", "battersFaced", "doubles", "earnedRuns", "era", "hitBatsmen", "hitByPitch", "hits", "homeRuns", "homeRunsPer9", "inheritedRunners", "inheritedRunnersScored", "intentionalWalks", "obp", "rbi", "runs", "runsScoredPer9", "sacBunts", "sacFlies", "stolenBasePercentage", "stolenBases", "triples", "whip", "wildPitches"

def mlb_games(*gamedates):
    for gamedate in gamedates:

        try:
            request = requests.get(f"http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={gamedate}").text
            request_json = json.loads(request)
            games = (request_json['dates'][0]['games'])
        except:
            continue

        for game in games:

            for category in categories:

                request = requests.get(f"http://statsapi.mlb.com{(game['link'])}").text
                request_json = json.loads(request)
                homeStats = (request_json['liveData']['boxscore']['teams']['home']['teamStats'][category])
                awayStats = (request_json['liveData']['boxscore']['teams']['away']['teamStats'][category])

                try:
                    if (game['teams']['home']['isWinner']) == True:
                        for key in homeStats.keys():
                            if key in pitching_stats_adjustment or batting_stats_adjustment:
                                if homeStats[key] < awayStats[key]:
                                    if category == 'batting':
                                        batting_winningStats.append(key)
                                    if category == 'pitching':
                                        pitching_winningStats.append(key)
                            else:
                                if homeStats[key] > awayStats[key]:
                                    if category == 'batting':
                                        batting_winningStats.append(key)
                                    if category == 'pitching':
                                        pitching_winningStats.append(key)
                    else:
                        for key in homeStats.keys():
                            if key in pitching_stats_adjustment or batting_stats_adjustment:
                                if awayStats[key] < homeStats[key]:
                                    if category == 'batting':
                                        batting_winningStats.append(key)
                                    if category == 'pitching':
                                        pitching_winningStats.append(key)
                            else:
                                if awayStats[key] > homeStats[key]:
                                    if category == 'batting':
                                        batting_winningStats.append(key)
                                    if category == 'pitching':
                                        pitching_winningStats.append(key)
                except:
                    continue

def dateRange(startDate,endDate):
    dates = []
    start = datetime.datetime.strptime(f"{startDate}", "%d-%m-%Y")
    end = datetime.datetime.strptime(f"{endDate}", "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    for date in date_generated:
        dates.append(date.strftime("%m/%d/%Y"))
    return(dates)

dates = dateRange(startDate,endDate)

for date in dates:
    mlb_games(date)

common_batting_winning_stats = (dict(Counter(batting_winningStats)))
common_pitching_winning_stats = (dict(Counter(pitching_winningStats)))

batting_stats_table = PrettyTable(['Stat', 'Amount of (Games) Winning Team Won the Category'])
pitching_stats_table = PrettyTable(['Stat', 'Amount of (Games) Winning Team Won the Category'])

for key, val in common_batting_winning_stats.items():
   batting_stats_table.add_row([key, val])

for key, val in common_pitching_winning_stats.items():
   pitching_stats_table.add_row([key, val])

batting_stats_table.sortby = 'Amount of (Games) Winning Team Won the Category'
pitching_stats_table.sortby = 'Amount of (Games) Winning Team Won the Category'
batting_stats_table.reversesort = True
pitching_stats_table.reversesort = True

print('\n\nCommon Winning Leading Batting Categories\n\n')
print(batting_stats_table)

print('\n\nCommon Winning Leading Pitching Categories\n\n')
print(pitching_stats_table)
