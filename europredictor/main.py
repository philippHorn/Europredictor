from flask import Flask, request, render_template, abort, url_for, redirect
from flask_bootstrap import Bootstrap
from match_data import get_all_teams
from datetime import datetime
#from graphing import sentiment_rolling_averages


app = Flask(__name__)
Bootstrap(app)

@app.route("/matches")
def matches():
    return render_template('matches.html', active = "matches")

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', active = "home")

@app.route("/graph/")
def graph():
    """page for showing a custom graph, specified in the GET-headers"""
    graph_keys = {"startMonth", "endMonth", "startDay", "endDay", "countries"}
    if graph_keys.intersection(request.args.keys()) == graph_keys:
        countries = request.args.getlist("countries")
        start_date, end_date = _get_times()
        #data_points = sentiment_rolling_averages(countries, start, end)

    return render_template('custom_graph.html', teams = get_all_teams(), active = "graph")

def _get_times():
    # todo: add validation, support for multiple formats
    s_month = request.args.get("startMonth", None)
    s_day = request.args.get("startDay", None)
    s_date = datetime.strptime(s_month + s_day + "2016", "%m%d%Y")
    e_month = request.args.get("endMonth", None)
    e_day = request.args.get("endDay", None)
    e_date = datetime.strptime(e_month + e_day + "2016", "%m%d%Y")
    return s_date, e_date


if __name__ == "__main__":
    app.run(debug=True)