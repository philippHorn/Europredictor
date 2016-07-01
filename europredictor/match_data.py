import requests
from datetime import datetime
from settings import BASE_DIR
import json

json_path =  BASE_DIR + "/europredictor/data/matchinfo.json"

with open(json_path) as file:
    json_str = file.read()
    js_dict = json.loads(json_str)
fixtures = js_dict['fixtures']


class Match:
    def __init__(self, json):
        self.start_date = datetime.strptime(json['date'], "%Y-%m-%dT%H:%M:%SZ")
        self.status = json['status']
        self.home_team = json['homeTeamName']
        self.away_team = json['awayTeamName']
        self.home_team_goals = json['result']["goalsHomeTeam"]
        self.away_team_goals = json['result']["goalsAwayTeam"]

class Team:
    def __init__(self, json):
        self.flag = json["crestUrl"]
        self.name = json["name"]

def get_all_matches():
    return [Match(match) for match in fixtures]
    
def get_past_matches():
    return [match for match in get_all_matches() if match.start_date < datetime.utcnow()]
    
def get_future_matches():
    return [match for match in get_all_matches() if match.start_date > datetime.utcnow()]

def get_all_teams():
    url = "http://api.football-data.org/v1/soccerseasons/424/teams"
    request = requests.get(url)
    teams = request.json()['teams']
    return [Team(team) for team in teams]


def update_info():
    global fixtures
    url = "http://api.football-data.org/v1/soccerseasons/424/fixtures"
    request = requests.get(url)
    with open(json_path, "w") as file:
        file.write(request.text)
    fixtures = request.json()
    