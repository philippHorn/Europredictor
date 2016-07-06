<h3>Overview</h3>
<p> The goal of this application is to provide insight about the general public's opinion about individual teams of the UEFA Euro 2016. To do that, we collected over 30000 comments or phrases from reddit, that contains references to countries participating in the tournament. Europredictor is able to present this data in form of a website (even though the website is currently not hosted), providing an easy interface to plot graphs. </p>
<br>
<h3> How it's done </h3>
The application contains a script that repeatedly calls the reddit API, collecting comments made on the soccer subreddit during the time of the tournament. If those comments refer to one country, we analyse the sentiment of the whole comment and save it into our database. If a comment countains references to multiple countries, it is split using natural language processing and the results are stored into the database individualy. Comments that don't refer to any country are ignored.
The collected data is presented on a website, which contains some pre-made graphs with some explanations and an interface to plot custom graphs from our data.
The application uses the following services and technologies:
<ul>
<li>The Reddit API and Praw as a wrapper for it</li>
<li>Sqlite3 for the database</li>
<li>Pandas to collect the sentiment data from the database and make it more presentable. Also for analyzing the data presented in the results page.</li>
<li>Python NLTK for sentiment analysis</li>
<li>The Pattern libary to split comments containing multiple countries</li>
<li>Flask for the server backend</li>
<li>Flask-Bootstrap to display the website to the users</li>
<li>Bokeh to make interactive graphs of the collected data</li>
<li>The Football Data API to get match times and results of the games</li>
</ul>
</p>
