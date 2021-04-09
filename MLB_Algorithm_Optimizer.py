# Author 
  # Brian Schroeder

# Synopsis
  # Get's the stat algorithm that leads to the highest percentage of winning for the projected team.
  
# Description
  # Each stat considered in the algorithm has been selected based off of the most common categories that the Winning Team Lead in after the victory.
  # The MLBWinAnalysis.py script gets all games for a range of dates and gets all the stats the team lead in with victory, which is used in this script to determine the most
  # effective combination of stats to predict the winning team
  
  # For Example, one simple algorithm is Home Batting average vs Away Batting Average and Home ERA vs Away ERA. This script will output the ammount of times 
  # the team has won factoring the simple algorithm provided. This script will do this for all of the possible unique algorithms and output the most effective combination.

from itertools import combinations
import requests
import json
from statistics import mean
from collections import Counter
from prettytable import PrettyTable
import datetime

#Format for Dates: Day,Month,Year
startDate = "02-04-2021"
endDate = "04-04-2021"

def dateRange(startDate,endDate):
    dates = []
    start = datetime.datetime.strptime(f"{startDate}", "%d-%m-%Y")
    end = datetime.datetime.strptime(f"{endDate}", "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    for date in date_generated:
        dates.append(date.strftime("%m/%d/%Y"))
    return(dates)

gameDates = dateRange(startDate,endDate)

analysis_comparison = []
for gameDate in gameDates:
    # Create Arrays
    mlb_teamStats = []
    mlb_advantages = []
    teamAdvatage = []
    projectedOutcome = []
    game_ids = []

    try:
        request = requests.get(f"http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={gameDate}").text
        request_json = json.loads(request)
        games = (request_json['dates'][0]['games'])
        for game in games:
            game_ids.append(game['gamePk'])
    except:
        continue

    for games in game_ids:
        homeBA = []
        awayBA = []
        homeSLG = []
        awaySLG = []
        homeOBP = []
        awayOBP = []
        game_analyzer = []

        request = requests.get(f"https://statsapi.mlb.com/api/v1/schedule?gamePk={games}&language=en&hydrate=lineups").text
        games_request_json = json.loads(request)
        try:
            (games_request_json['dates'][0]['games'][0]['lineups']['homePlayers'])
        except:
            continue

        try:
            (games_request_json['dates'][0]['games'][0]['lineups']['awayPlayers'])
        except:
            continue

        homeTeamName = (games_request_json['dates'][0]['games'][0]['teams']['home']['team']['name'])
        awayTeamName = (games_request_json['dates'][0]['games'][0]['teams']['away']['team']['name'])
        homeTeam = (games_request_json['dates'][0]['games'][0]['lineups']['homePlayers'])
        awayTeam = (games_request_json['dates'][0]['games'][0]['lineups']['awayPlayers'])

        # Getting Batters Career Averages
        for player in homeTeam:
            try:
                id = (player['id'])
                request = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id='{id}'").text
                request_json = json.loads(request)
                playerStats = (request_json['sport_career_hitting']['queryResults']['row'])
                homeBA.append(float(playerStats['avg']))
                homeSLG.append(float(playerStats['slg']))
                homeOBP.append(float(playerStats['obp']))
            except:
                continue
        for player in awayTeam:
            try:
                id = (player['id'])
                request = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id='{id}'").text
                request_json = json.loads(request)
                playerStats = (request_json['sport_career_hitting']['queryResults']['row'])
                awayBA.append(float(playerStats['avg']))
                awaySLG.append(float(playerStats['slg']))
                awayOBP.append(float(playerStats['obp']))
            except:
                continue

        # Get Starting Pitcher Stats
        try:
            pitcherRequest = requests.get(f"http://statsapi.mlb.com/api/v1/game/{games}/boxscore").text
            pitcher_json = json.loads(pitcherRequest)

            homePitcher = pitcher_json['teams']['home']['pitchers'][0]
            awayPitcher = pitcher_json['teams']['away']['pitchers'][0]

            homePitcherRequest = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_pitching.bam?league_list_id='mlb'&game_type='R'&player_id='{homePitcher}'").text
            homepitcherRequest_json = json.loads(homePitcherRequest)
            awayPitcherRequest = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_pitching.bam?league_list_id='mlb'&game_type='R'&player_id='{awayPitcher}'").text
            awaypitcherRequest_json = json.loads(awayPitcherRequest)

            homePitcherStats = (homepitcherRequest_json['sport_career_pitching']['queryResults']['row'])
            awayPitcherStats = (awaypitcherRequest_json['sport_career_pitching']['queryResults']['row'])
        except:
            continue

        advantages = {
            'Home Team': homeTeamName,
            "Away Team": awayTeamName,
            "Home BA": round(mean(homeBA) - mean(awayBA), 3),
            "Home Slugging %": round(mean(homeSLG) - mean(awaySLG), 3),
            "Home OBP %": round(mean(homeOBP) - mean(awayOBP), 3),
            "Home ERA": round(float(homePitcherStats['era']) - float(awayPitcherStats['era']), 3) * -1,
            "Home WHIP": round(float(homePitcherStats['whip']) - float(awayPitcherStats['whip']), 3) * -1,
            "Home OBP Against": (round(float(homePitcherStats['obp']), 2) - round(float(awayPitcherStats['obp']), 2)) * -1,
            "Home Homeruns/9 Against": (round(float(homePitcherStats['h9']), 2) - round(float(awayPitcherStats['h9']),2)) * -1,
            "Home BB/9 Against": (round(float(homePitcherStats['bb9']), 2) - round(float(awayPitcherStats['bb9']), 2)) * -1,
            "Away BA": round(mean(awayBA) - mean(homeBA), 3),
            "Away Slugging %": round(mean(awaySLG) - mean(homeSLG), 3),
            "Away OBP %": round(mean(awayOBP) - mean(homeOBP), 3),
            "Away ERA": round(float(awayPitcherStats['era']) - float(homePitcherStats['era']), 3) * -1,
            "Away WHIP": round(float(awayPitcherStats['whip']) - float(homePitcherStats['whip']), 3) * -1,
            "Away OBP Against": (round(float(awayPitcherStats['obp']), 2) - round(float(homePitcherStats['obp']), 2)) * -1,
            "Away Homeruns/9 Against": (round(float(awayPitcherStats['h9']), 2) - round(float(homePitcherStats['h9']),2)) * -1,
            "Away BB/9 Against": (round(float(awayPitcherStats['bb9']), 2) - round(float(homePitcherStats['bb9']), 2)) * -1,
        }

        homeAdvantage = advantages['Home BA'] + advantages['Home Slugging %'] + advantages['Home OBP %'] + advantages['Home ERA'] + advantages['Home WHIP'] + advantages['Home Homeruns/9 Against'] + advantages['Home OBP Against'] + advantages['Home BB/9 Against']
        awayAdvantage = advantages['Away BA'] + advantages['Away Slugging %'] + advantages['Away OBP %'] + advantages['Away ERA'] + advantages['Away WHIP'] + advantages['Away Homeruns/9 Against'] + advantages['Away OBP Against'] + advantages['Away BB/9 Against']


        try:
            if (games_request_json['dates'][0]['games'][0]['teams']['home']['isWinner']) == True:
                homeWinner = 'Yes'
            elif (games_request_json['dates'][0]['games'][0]['teams']['home']['isWinner']) == False:
                homeWinner = 'No'
            else:
                homeWinner = 'TBD'

            if (games_request_json['dates'][0]['games'][0]['teams']['away']['isWinner']) == True:
                awayWinner = 'Yes'
            elif (games_request_json['dates'][0]['games'][0]['teams']['away']['isWinner']) == False:
                awayWinner = 'No'
            else:
                awayWinner = 'TBD'
        except:
            continue

        # Define Stats to Create Algorithm for
        homeInput = "advantages['Home BA'] > advantages['Away BA']", "advantages['Home Slugging %'] > advantages['Away Slugging %']", "advantages['Home OBP %'] > advantages['Away OBP %']", "advantages['Home ERA'] > advantages['Away ERA']", "advantages['Home WHIP'] > advantages['Away WHIP']", "advantages['Home Homeruns/9 Against'] > advantages['Away Homeruns/9 Against']", "advantages['Home OBP Against'] > advantages['Away OBP Against'] ", "advantages['Home BB/9 Against'] > advantages['Away BB/9 Against']"
        awayInput = "advantages['Away BA'] > advantages['Home BA']", "advantages['Away Slugging %'] > advantages['Home Slugging %']", "advantages['Away OBP %'] > advantages['Home OBP %']", "advantages['Away ERA'] > advantages['Home ERA']", "advantages['Away WHIP'] > advantages['Home WHIP']", "advantages['Away Homeruns/9 Against'] > advantages['Home Homeruns/9 Against']", "advantages['Away OBP Against'] > advantages['Home OBP Against'] ", "advantages['Away BB/9 Against'] > advantages['Home BB/9 Against']"

        # Get All Possible Combinations of Stats to be Analyzed
        homeoutput = sum([list(map(list, combinations(homeInput, i))) for i in range(len(homeInput) + 1)], [])
        awayoutput = sum([list(map(list, combinations(awayInput, i))) for i in range(len(awayInput) + 1)], [])

        if homeWinner == 'Yes':
            # Put all Possible Combinations in Operator Format
            for stat_Array in homeoutput:
                algorithm = ''
                for stat in stat_Array:
                    if (len(stat_Array)) == 1:
                        algorithm += (stat)
                    else:
                        stat = stat + ' and '
                        algorithm += stat
                if 'and' in algorithm:
                    algorithm = algorithm[:-5]

                try:
                    if eval(algorithm):
                        projectedWinner = {
                            'Projected Winner': advantages['Home Team'],
                            'Winner Advantage (Beta)': homeAdvantage,
                            'Opponent': advantages['Away Team'],
                            'Opponent Deficit': awayAdvantage,
                            'Winner': homeWinner,
                            'Score': f"{advantages['Home Team']}: {games_request_json['dates'][0]['games'][0]['teams']['home']['score']}  {advantages['Away Team']}: {games_request_json['dates'][0]['games'][0]['teams']['away']['score']} ",
                            'Algorithm': algorithm
                        }

                        analysis_comparison.append(projectedWinner['Algorithm'])
                except:
                    continue
        else:
            # Put all Possible Combinations in Operator Format
            for stat_Array in awayoutput:
                algorithm = ''
                for stat in stat_Array:
                    if (len(stat_Array)) == 1:
                        algorithm += (stat)
                    else:
                        stat = stat + ' and '
                        algorithm += stat
                if 'and' in algorithm:
                    algorithm = algorithm[:-5]

                try:
                    if eval(algorithm):
                        projectedWinner = {
                            'Projected Winner': advantages['Away Team'],
                            'Winner Advantage (Beta)': awayAdvantage,
                            'Opponent': advantages['Home Team'],
                            'Opponent Deficit': homeAdvantage,
                            'Winner': awayWinner,
                            'Score': f"{advantages['Away Team']}: {games_request_json['dates'][0]['games'][0]['teams']['away']['score']}  {advantages['Home Team']}: {games_request_json['dates'][0]['games'][0]['teams']['home']['score']} ",
                            'Algorithm': algorithm
                        }

                        analysis_comparison.append(projectedWinner['Algorithm'])
                except:
                    continue

algorithm_Analyzer = (dict(Counter(analysis_comparison)))
algorithm_Analyzer_Table = PrettyTable(['Stat', 'Amount of (Games) Winning Team Won the Category'])
for val, key in algorithm_Analyzer.items():
   algorithm_Analyzer_Table.add_row([val, key])
print(algorithm_Analyzer_Table)
