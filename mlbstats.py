import requests
import json

def mlb_schedule():
    game_ids = []
    request = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date=04/02/2021").text
    request_json = json.loads(request)
    games = (request_json['dates'][0]['games'])
    for game in games:
        game_ids.append(game['gamePk'])
    return game_ids

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

    stats = {
        'Home Team': homeTeamName,
        'Away Team': awayTeamName,
        'Home Batting Average': sum(homeBA),
        'Away Batting Average': sum(awayBA)
    }

    print(stats)
