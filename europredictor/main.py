from flask import Flask, request, render_template, abort
from flask_bootstrap import Bootstrap
from match_data import get_all_teams
#from graphing import sentiment_rolling_averages


app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return render_template('test.html', teams = get_all_teams())

@app.route("/graph/")
def graph():
    """page for showing a custom graph, specified in the GET-headers"""
    print request.args.getlist("countries")
    print "-------"
    countries = request.args.getlist("countries")
    #start = request.args.get("start", None)
    #end = request.args.get("end", None)
    if not countries:
        abort(400)
    data_points = sentiment_rolling_averages(countries, start, end)

    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)