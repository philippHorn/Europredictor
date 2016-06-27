from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/graph/")
def graph():
    """page for showing a custom graph, specified in the GET-headers"""
    countries = request.args.getlist("countries")
    start = request.args.get("start", None)
    end = request.args.get("end", None)
    assert countries and start and end, "Invalid request"
    data_points = sentiment_data_points(countries, start, end)

    return "Graph"

if __name__ == "__main__":
    app.run(debug=True)