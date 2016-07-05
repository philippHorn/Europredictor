import pandas as pd
from keywords import keywords
from datetime import datetime
from bokeh.charts import TimeSeries, output_file, show, Bar
from db_IO import read_to_dataframe
from bokeh.embed import components
from flask import abort
from pprint import pprint

def prepare_df(countries = None, start_time = 0, end_time = None):
    '''reads and prepares dataframe'''

    if end_time is None:
        end_time = datetime.now()
        
    # Creat the dataframe from the database
    df = read_to_dataframe(countries = countries, start_time = start_time, end_time = end_time)
    if df.empty:
        return
        
    # Calculate the overall sentiment
    df['sentiment'] = df.pos_sentiment - df.neg_sentiment
    
    # Delete the columns we don't need
    df.drop('pos_sentiment', axis=1, inplace=True)
    df.drop('neg_sentiment', axis=1, inplace=True)
    
    # Convert from unix timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    return  df

def plot_countries(countries, start_time, end_time, smoothen = False):
    
    df = prepare_df(countries = countries, start_time = start_time, end_time = end_time)

    if df is None:
        abort(400)

    if smoothen:
        groups = df.groupby('name')

        dfs = []
        for name, dataf in groups:
            # window size should be proportional to the number of data points
            # 30 was found to work nice through experimentation
            w_size = int((dataf['sentiment'].size/30.0))    
            dataf['sentiment'] = pd.rolling_mean(dataf['sentiment'], w_size)
            dfs.append(dataf)

        df = pd.concat(dfs)
        
    p = TimeSeries(df, x='timestamp', y='sentiment', color='name', width=1200)
    return "\n".join(components(p))

def get_other_stats():
    "this function produces the graphs contained in the 'home' page"
    
    df = prepare_df(countries = keywords.keys(), 
                    start_time = datetime(2016, 6, 10).strftime("%s"), # euros start date
                    end_time = datetime(2016, 7, 10).strftime("%s")) # euros end date
    groups = df.groupby('name')
    
    print "Sorted country means:"
    means = [(name, dataf['sentiment'].mean()) for name, dataf in groups]
    pprint (sorted(means, key = lambda x: x[1]))
    
    print "Sorted controversy (uses mean absolute deviation):"
    convs = [(name, dataf['sentiment'].mad()) for name, dataf in groups]
    pprint (sorted(convs, key = lambda x: x[1]))
    
    print "Sorted by number of comments"
    sizes = [(name, dataf['sentiment'].size) for name, dataf in groups]
    pprint (sorted(sizes, key = lambda x: x[1]))
    
    print "Sorted by change in general opinion:"
    changes = [(name, _get_change(dataf))for name, dataf in groups]
    pprint (sorted(changes, key = lambda x: x[1]))
    
    values = [means, convs, sizes, changes]
    labels = ["mean", "controversy", "comments", "mean difference"]
    
    for vals, label in zip(values, labels):
        data = {
            label : [v[1] for v in vals],
            "labels" : [v[0] for v in vals]
            }
        bar = Bar(data, values = label, label = "labels")
        with open("europredictor/templates/plots/" + label + ".html", "w") as file:
            file.write("\n".join(components(bar)))

    
def _get_change(dataf):
    sent_series = dataf['sentiment']
    size = sent_series.size - 1
    start_mean = sent_series[:size/8].mean()
    end_mean = sent_series[int(size * (7.0/8)):].mean()
    return start_mean - end_mean
    
#get_other_stats()