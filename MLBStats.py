import requests
import json
import pandas as pd
import datetime
from statistics import mean

todaysGames = datetime.datetime.now().strftime("%m/%d/%Y")

def mlb_schedule():
    game_ids = []

    request = requests.get(f"http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={todaysGames}").text
    request_json = json.loads(request)
    games = (request_json['dates'][0]['games'])
    for game in games:
        game_ids.append(game['gamePk'])
    return game_ids

mlb_teamStats = []
mlb_advantages = []
teamAdvatage = []
projectedOutcome = []

for games in mlb_schedule():
    homeBA = []
    awayBA = []
    homeSLG = []
    awaySLG = []
    homeOBP = []
    awayOBP = []

    request = requests.get(f"https://statsapi.mlb.com/api/v1/schedule?gamePk={games}&language=en&hydrate=lineups").text
    request_json = json.loads(request)
    try:
        (request_json['dates'][0]['games'][0]['lineups']['homePlayers'])
    except:
        continue

    try:
        (request_json['dates'][0]['games'][0]['lineups']['awayPlayers'])
    except:
        continue

    homeTeamName = (request_json['dates'][0]['games'][0]['teams']['home']['team']['name'])
    awayTeamName = (request_json['dates'][0]['games'][0]['teams']['away']['team']['name'])
    homeTeam = (request_json['dates'][0]['games'][0]['lineups']['homePlayers'])
    awayTeam = (request_json['dates'][0]['games'][0]['lineups']['awayPlayers'])

    # Getting Batters Carrer Averages
    for player in homeTeam:
        try:
            id = (player['id'])
            request = requests.get(
                f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id='{id}'").text
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
            request = requests.get(
                f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id='{id}'").text
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

        homePitcherRequest = requests.get(
            f"http://lookup-service-prod.mlb.com/json/named.sport_career_pitching.bam?league_list_id='mlb'&game_type='R'&player_id='{homePitcher}'").text
        homepitcherRequest_json = json.loads(homePitcherRequest)
        awayPitcherRequest = requests.get(
            f"http://lookup-service-prod.mlb.com/json/named.sport_career_pitching.bam?league_list_id='mlb'&game_type='R'&player_id='{awayPitcher}'").text
        awaypitcherRequest_json = json.loads(awayPitcherRequest)

        homePitcherStats = (homepitcherRequest_json['sport_career_pitching']['queryResults']['row'])
        awayPitcherStats = (awaypitcherRequest_json['sport_career_pitching']['queryResults']['row'])
    except:
        continue

    stats = {
        'Home Team': homeTeamName,
        "Away Team": awayTeamName,
        "Home Batting Average": round(sum(homeBA), 2),
        "Home Slugging %": round(sum(homeSLG), 3),
        "Home OBP %": round(sum(homeOBP), 3),
        "Home Starting ERA": round(float(homePitcherStats['era']), 2),
        "Home Starting WHIP": round(float(homePitcherStats['whip']), 2),
        "Away Batting Average": round(sum(awayBA), 3),
        "Away Slugging %": round(sum(homeSLG), 3),
        "Away OBP %": round(sum(awayOBP), 3),
        "Away Starting ERA": round(float(awayPitcherStats['era']), 2),
        "Away Starting WHIP": round(float(awayPitcherStats['whip']), 2)
    }

    advantages = {
        'Home Team': homeTeamName,
        "Away Team": awayTeamName,
        "Home BA": round(sum(homeBA) - sum(awayBA), 3),
        "Home Slugging %": round(sum(homeSLG) - sum(awaySLG), 3),
        "Home OBP %": round(sum(homeOBP) - sum(awayOBP), 3),
        "Home ERA": round(float(homePitcherStats['era']) - float(awayPitcherStats['era']), 3) * -1,
        "Home WHIP": round(float(homePitcherStats['whip']) - float(awayPitcherStats['whip']), 3) * -1,
        "Away BA": round(sum(awayBA) - sum(homeBA), 3),
        "Away Slugging %": round(sum(awaySLG) - sum(homeSLG), 3),
        "Away OBP %": round(sum(awayOBP) - sum(homeOBP), 3),
        "Away ERA": round(float(awayPitcherStats['era']) - float(homePitcherStats['era']), 3) * -1,
        "Away WHIP": round(float(awayPitcherStats['whip']) - float(homePitcherStats['whip']), 3) * -1
    }

    #Get Game Info
    game_request = requests.get(f"http://statsapi.mlb.com/api/v1.1/game/{games}/feed/live").text
    game_info = json.loads(game_request)

    if (advantages['Home BA']) > (advantages['Away BA']) and (advantages['Home ERA']) > (advantages['Away ERA']) and (advantages['Home WHIP']) > (advantages['Away WHIP']) and (advantages['Home Slugging %']) > (advantages['Away Slugging %']) and (advantages['Home OBP %']) > (advantages['Away OBP %']):
        projectedWinner = {
            'Projected Winner': advantages['Home Team'],
            'Opponent': advantages['Away Team'],
            'First Pitch': f"{game_info['gameData']['datetime']['time']} {game_info['gameData']['datetime']['ampm']}",
            'Project Winning Team Probable Pitcher': game_info['gameData']['probablePitchers']['home']['fullName'],
            'Project Oponent Team Probable Pitcher': game_info['gameData']['probablePitchers']['away']['fullName'],
            'Weather': f"{game_info['gameData']['weather']['temp']}, {game_info['gameData']['weather']['condition']}"
        }
        projectedOutcome.append(projectedWinner)

    if (advantages['Away BA']) > (advantages['Home BA']) and (advantages['Away ERA']) > (advantages['Home ERA']) and (advantages['Away WHIP']) > (advantages['Home WHIP']) and (advantages['Away Slugging %']) > (advantages['Home Slugging %']) and (advantages['Away OBP %']) > (advantages['Home OBP %']):
        projectedWinner = {
            'Projected Winner': advantages['Away Team'],
            'Opponent': advantages['Home Team'],
            'First Pitch': f"{game_info['gameData']['datetime']['time']} {game_info['gameData']['datetime']['ampm']}",
            'Project Winning Team Probable Pitcher': game_info['gameData']['probablePitchers']['away']['fullName'],
            'Project Oponent Team Probable Pitcher': game_info['gameData']['probablePitchers']['home']['fullName'],
            'Weather': f"{game_info['gameData']['weather']['temp']}, {game_info['gameData']['weather']['condition']}"
        }
        projectedOutcome.append(projectedWinner)

    mlb_teamStats.append(stats)
    mlb_advantages.append(advantages)

projectedOutcome_dataframe = pd.DataFrame(data=projectedOutcome)
stats_dataframe = pd.DataFrame(data=mlb_teamStats)
stats_dataframe_sorted = stats_dataframe.sort_values(by='Home Team')
advantages_dataframe = pd.DataFrame(data=mlb_advantages)
advantages_dataframe_sorted = advantages_dataframe.sort_values(by='Home Team')

todaysDate = datetime.datetime.now().strftime("%A, %B %d, %Y")
updateTime = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S")

htmlgameanalysis = "<h1>Game Analysis</h1>"

for team in teamAdvatage:
    htmlgameanalysis += (team)

# Setup HTML for Webpage
htmlheader = "<br></br> <h1> Team Advantages </h1>"
htmlheader2 = "<h1>Team Statistics</h1>"

htmltop = f"""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="./MLBStyle.css">
<link href="style.css?t=[timestamp]" type="text/css" rel="stylesheet">
<h2> Games for: {todaysDate} </h2>
</head>
<body>
"""

htmlbottom = f"""
<br> </br>
<h4> Updated Time: {updateTime} </h4>
</body>
</html>
"""

# Export Tables to HTML Page
with open('/var/www/html/index.html', 'w') as _file:
    _file.write(htmltop + htmlgameanalysis + projectedOutcome_dataframe.to_html(index=False, col_space=100) + htmlheader + advantages_dataframe_sorted.to_html(index=False, col_space=100) + htmlheader2 + stats_dataframe_sorted.to_html(index=False, col_space=100) + htmlbottom)
