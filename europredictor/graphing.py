import pandas as pd
from datetime import datetime
from bokeh.charts import TimeSeries, output_file, show
from db_IO import read_to_dataframe
from bokeh.embed import components
from flask import abort

def prepare_df(countries = None, start_time = 0, end_time = None):
    '''reads and prepares dataframe'''

    if end_time is None:
        end_time = datetime.now()
        
    # Creat the dataframe from the database
    df = read_to_dataframe(countries = countries, average = False, start_time = start_time, end_time = end_time)
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
        group = df.groupby('name')

        dfs = []
        for name, dataf in group:
            # window size should be proportional to the number of data points
            # 30 was found to work nice through experimentation
            w_size = int((dataf['sentiment'].size/30.0))    
            dataf['sentiment'] = pd.rolling_mean(dataf['sentiment'], w_size)
            dfs.append(dataf)

        df = pd.concat(dfs)
        
    p = TimeSeries(df, x='timestamp', y='sentiment', color='name', width=1200)
    return "\n".join(components(p))

