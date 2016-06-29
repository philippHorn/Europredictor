from flask import Flask, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/graph/")
def graph():
    """page for showing a custom graph, specified in the GET-headers"""
    countries = request.args.getlist("countries")
    start = request.args.get("start", None)
    end = request.args.get("end", None)
    if not (countries and start and end): 
        abort(400)
    data_points = sentiment_data_points(countries, start, end)

    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)