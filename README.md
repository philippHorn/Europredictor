<h3>Overview</h3>
<p> The goal of this application is to provide insight about the general public's opinion about individual teams of the UEFA Euro 2016. To do that, we collected over 30000 comments or phrases from reddit, that contain references to countries participating in the tournament. Europredictor is able to present this data in form of a website (even though the website is currently not hosted), providing an easy interface to plot graphs. </p>
<br>

<h3>Results</h3>
<p>According to our data, Hungary was the most popular country during the tournament, while Russia was the least popular. This was done by taking the mean for each countries sentiment.
<img src="http://i.imgur.com/HVJAzb5.png"></img><br>
Russia had the greatest positive change in people's general opinion, Croatia had the greatest negative change. To get to these results we compared a country's mean for the oldest quarter of their comments to the mean of the latest quarter of their comments. The graph contains the first quarter's mean minus the last quarter's mean.
<img src="http://i.imgur.com/nGN7OcV.png"></img><br>
In Croatias graph there is a huge drop visible on the 18th June. This was during a match were Croatias fans interrupted the game by throwing flares onto the field.
<img src="http://i.imgur.com/MjrWLnl.png"></img><br>
Out of all countries, England was mentioned the most and Czech Republic was mentioned the least. The wide gap between England and the other countries can be explained by us always counting the word "English" as referring to the English team, while the term often refers to the English language. So there might be quite a few falsely recognized comments about England in our database.<br>
<img src="http://i.imgur.com/HG91DpA.png"></img>
</p>
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
<li>The Football Data API to get start times and results for the games</li>
</ul>
</p>
<br>
<h3>Improvement Aspects</h3>
<p>The biggest issue of the application is the analysis of the comments. Sometimes the country reference has no connection to the sentiment and we fail to recognize that. Sentences like "He played really well in his match against Italy" will mistakenly result in a positive score for Italiy. The sentiment analyser is also trained on data from movie reviews and twitter and sometimes fails to make sense of the language and references used in the captured reddit comments. This could be improved by using lower level natural language processing.<br>
</p>
<h3>Contributers</h3>
<ul>
<li>Ben https://github.com/balmf</li>
<li>Philipp https://github.com/philippHorn</li>
<li>Elliot https://github.com/cupcakehunter</li>

</ul>
