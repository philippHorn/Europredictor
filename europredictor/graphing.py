import pandas as pd
from datetime import datetime
from bokeh.charts import TimeSeries, output_file, show
from db_IO import read_to_dataframe
from bokeh.embed import components
from flask import abort

def sentiment_rolling_averages(countries = None, interval = 'hour', start_time = 0, end_time = None):
    '''



    '''
    if end_time is None:
        end_time = datetime.now()
        
    # Creat the dataframe from the database
    df = read_to_dataframe(countries = countries, average = False, start_time = start_time, end_time = end_time)
    if df.empty:
        abort(400)
        
    # Calculate the overall sentiment
    df['sentiment'] = df.pos_sentiment - df.neg_sentiment
    
    # Delete the columns we don't need
    df.drop('pos_sentiment', axis=1, inplace=True)
    df.drop('neg_sentiment', axis=1, inplace=True)
    
    # Convert from unix timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    
    #This doesn't seem to be working yet - and it's not a rolling average.
    #df = df.groupby([df["name"], df["timestamp"].dt.hour]).mean()
    

    return df

def plot_countries(countries, start_time, end_time, smoothen = False):
    
    df = sentiment_rolling_averages(countries = countries, start_time = start_time, end_time = end_time, interval = 'hour')
    if smoothen:
        group = df.groupby('name')
        dfs = []
        for name, dataf in group:
            dataf['sentiment'] = pd.rolling_mean(dataf['sentiment'], 20)
            dfs.append(dataf)
        df = pd.concat(dfs)
        
    p = TimeSeries(df, x='timestamp', y='sentiment', color='name', width=1200)
    return "\n".join(components(p))

