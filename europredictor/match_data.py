import requests
from datetime import datetime
from settings import BASE_DIR
import json

GROUP_STAGE_END = datetime(2016, 6, 23)
ROUND_16_END = datetime(2016, 6, 28)
QUARTER_FINAL_END = datetime(2016, 7, 4)
SEMI_FINAL_END = datetime(2016, 7, 8)
FINAL_END = datetime(2016, 7, 11)

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
    
def get_match(start_date):
    return [match for match in get_all_matches() if match.start_date == start_date][0]
    
def get_past_matches(grouped = False):
    if grouped: 
        matches = get_past_matches()
        return {
            "Group Stage" : [match for match in matches if match.start_date < GROUP_STAGE_END],
            "Round of 16" : [match for match in matches if GROUP_STAGE_END < match.start_date < ROUND_16_END],
            "Quarter Final" : [match for match in matches if ROUND_16_END < match.start_date < QUARTER_FINAL_END],
            "Semi Final" : [match for match in matches if QUARTER_FINAL_END < match.start_date < SEMI_FINAL_END],
            "Final" : [match for match in matches if SEMI_FINAL_END < match.start_date < FINAL_END]
        }
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
    
