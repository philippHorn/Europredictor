from flask import Flask, request, render_template, abort, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from keywords import keywords
from datetime import datetime
from graphing import plot_countries
from match_data import get_past_matches, get_match
from settings import SECRET_KEY

HOUR_TSTAMP = 60 * 60.0

app = Flask(__name__)
Bootstrap(app)

@app.route("/matches/")
def matches():
    graph = ""
    match = None
    start_date = request.args.get("matchStart", None)
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        start_tstamp = float(start_date.strftime("%s"))
        match = get_match(start_date)
        countries = [match.away_team, match.home_team]
        smoothen = "noise" in request.args
        
        # get the graph with some extra time before and after the match
        graph = plot_countries(countries, 
                               start_tstamp - HOUR_TSTAMP * 6, 
                               start_tstamp + HOUR_TSTAMP * 5, 
                               smoothen = smoothen)
        
        
    matches = get_past_matches(grouped = True)
    return render_template('matches.html', active = "matches", 
                           matches = matches, graph = graph, match = match)

@app.route("/")
@app.route("/home/")
def home():
    return render_template('home.html', active = "home")

@app.route("/graph/")
def graph():
    """page for showing a custom graph, specified in the GET-headers"""
    
    graph_keys = {"startMonth", "endMonth", "startDay", "endDay", "countries"}
    graph = ""
    if graph_keys.intersection(request.args.keys()) == graph_keys:
        countries = request.args.getlist("countries")
        start_date, end_date = _get_times()
        s_timestamp = float(start_date.strftime("%s")) 
        e_timestamp = float(end_date.strftime("%s"))
        smoothen = "noise" in request.args
        graph = plot_countries(countries, s_timestamp, e_timestamp, smoothen = smoothen)
        
    return render_template('custom_graph.html', 
                            teams = sorted(keywords.keys()), 
                            active = "graph", 
                            graph = graph)

def _get_times():
    "return the dates from GET-request as datetime objects"
    
    s_month = request.args.get("startMonth", None)
    s_day = request.args.get("startDay", None)
    s_date = datetime.strptime(s_month + s_day + "2016", "%m%d%Y")
    e_month = request.args.get("endMonth", None)
    e_day = request.args.get("endDay", None)
    e_date = datetime.strptime(e_month + e_day + "2016", "%m%d%Y")
    return s_date, e_date

@app.errorhandler(400)
def invalid_graph(error):
    flash("Invalid Request, there is no data for the specified timeframe on the specified countries.")
    return redirect(url_for('graph'))

if __name__ == "__main__":
    import os
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.secret_key = SECRET_KEY
    app.run(debug=False, host=host, port=port)
