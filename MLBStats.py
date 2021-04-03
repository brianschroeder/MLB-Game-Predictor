import requests
import json
import pandas as pd
import datetime 

todaysGames = datetime.datetime.now().strftime("%m/%d/%Y")
updateTime = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S")

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

for games in mlb_schedule():
    homeBA = []
    awayBA = []
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
            request = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id='{id}'").text
            request_json = json.loads(request)
            playerStats = (request_json['sport_career_hitting']['queryResults']['row'])
            homeBA.append(float(playerStats['avg']))
        except:
            continue
    for player in awayTeam:
        try:
            id = (player['id'])
            request = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id='{id}'").text
            request_json = json.loads(request)
            playerStats = (request_json['sport_career_hitting']['queryResults']['row'])
            awayBA.append(float(playerStats['avg']))
        except:
            continue

    #Get Starting Pitcher Stats
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

    stats = {
        'Home Team': homeTeamName,
        "Away Team": awayTeamName,
        "Home Batting Average": round(sum(homeBA), 2),
        "Home Starting ERA": round(float(homePitcherStats['era']), 2),
        "Home Starting WHIP": round(float(homePitcherStats['whip']), 2),
        "Away Batting Average": round(sum(awayBA), 2),
        "Away Starting ERA": round(float(awayPitcherStats['era']), 2),
        "Away Starting WHIP": round(float(awayPitcherStats['whip']), 2)
    }

    advantages = {
        'Home Team': homeTeamName,
        "Away Team": awayTeamName,
        "Home BA Advantage": round(sum(homeBA) - sum(awayBA), 2),
        "Home ERA Advantage": round(float(homePitcherStats['era']) - float(awayPitcherStats['era']), 2) * -1,
        "Home WHIP Advantage": round(float(homePitcherStats['whip']) - float(awayPitcherStats['whip']), 2) * -1,
        "Away BA Advantage": round(sum(awayBA) - sum(homeBA), 2),
        "Away ERA Advantage": round(float(awayPitcherStats['era']) - float(homePitcherStats['era']), 2) * -1,
        "Away WHIP Advantage": round(float(awayPitcherStats['whip']) - float(homePitcherStats['whip']), 2) * -1
    }

    mlb_teamStats.append(stats)
    mlb_advantages.append(advantages)

stats_dataframe = pd.DataFrame(data=mlb_teamStats)
stats_dataframe_sorted = stats_dataframe.sort_values(by='Home Team')
advantages_dataframe = pd.DataFrame(data=mlb_advantages)
advantages_dataframe_sorted = advantages_dataframe.sort_values(by='Home Team')

# Set Pandas Table Output Sizing
pd.set_option('display.max_rows', 700)
pd.set_option('display.max_columns', 700)
pd.set_option('display.width', 350)

#Setup HTML for Webpage
htmlheader = "<h1>Team Statistics</h1>"
htmlheader2 = "<br></br> <h1> Team Advantages </h1>"

htmltop = f"""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="./MLBStyle.css">
<h3> Games for: {todaysgames} </h3>
</head>
<body>

"""

htmlbottom = f"""
<br> </br> <br></br>
Update Time: {updateTime}
</body>
</html>
"""

#Export Tables to HTML Page
with open('/var/www/html/index.html', 'w') as _file:
    _file.write(htmltop + htmlheader + stats_dataframe_sorted.to_html(index=False, col_space=100) + htmlheader2 + advantages_dataframe_sorted.to_html(index=False, col_space=100) + htmlbottom)
