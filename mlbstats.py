import requests
import json
from prettytable import PrettyTable
from prettytable import from_html_one

def mlb_schedule():
    game_ids = []
    request = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date=04/02/2021").text
    request_json = json.loads(request)
    games = (request_json['dates'][0]['games'])
    for game in games:
        game_ids.append(game['gamePk'])
    return game_ids

mlb_teamStats = []

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

    stats = [
        homeTeamName,
        awayTeamName,
        round(sum(homeBA), 2),
        round(sum(awayBA), 2),
        round(float(homePitcherStats['era']), 2),
        round(float(awayPitcherStats['era']), 2),
        round(float(homePitcherStats['whip']), 2),
        round(float(awayPitcherStats['whip']), 2),
        round(sum(homeBA) - sum(awayBA), 2) * -1,
        round(sum(awayBA) - sum(homeBA), 2) * -1,
        round(float(homePitcherStats['era']) - float(awayPitcherStats['era']), 2) * -1,
        round(float(awayPitcherStats['era']) - float(homePitcherStats['era']), 2) * -1,
        round(float(homePitcherStats['whip']) - float(awayPitcherStats['whip']), 2) * -1,
        round(float(awayPitcherStats['whip']) - float(homePitcherStats['whip']), 2) * -1
    ]

    mlb_teamStats.append(stats)

myTable = PrettyTable(["Home Team", "Away Team", "Home Batting Average", "Away Batting Average","Home Starting ERA", "Away Starting ERA" , "Home Starting WHIP", "Away Starting WHIP", "Home BA Advantage", "Away BA Advantage", "Home ERA Advantage", "Away ERA Advantage", "Home WHIP Advantage", "Away WHIP Advantage"])

for team in mlb_teamStats:
   myTable.add_row((team))

print(myTable)
