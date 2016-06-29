import pandas as pd
from datetime import datetime
from bokeh.charts import TimeSeries, output_file, show
from db_IO import read_to_dataframe


def sentiment_rolling_averages(countries = None, interval = 'hour', start_time = 0, end_time = datetime.now()):
    '''



    '''
    # Creat the dataframe from the database
    df = read_to_dataframe(countries = countries, average = False, start_time = start_time, end_time = end_time)
    
    # Calculate the overall sentiment
    df['sentiment'] = df.pos_sentiment - df.neg_sentiment
    
    # Delete the columns we don't need
    df.drop('id', axis=1, inplace=True)
    df.drop('thread_title', axis=1, inplace=True)
    df.drop('thread_url', axis=1, inplace=True)
    df.drop('comment_url', axis=1, inplace=True)
    df.drop('username', axis=1, inplace=True)
    df.drop('comment', axis=1, inplace=True)
    df.drop('neu_sentiment', axis=1, inplace=True)
    df.drop('comp_sentiment', axis=1, inplace=True)
    df.drop('pos_sentiment', axis=1, inplace=True)
    df.drop('neg_sentiment', axis=1, inplace=True)
    
    # Convert from unix timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    
    #This doesn't seem to be working yet - and it's not a rolling average.
    df.groupby([df["country"], df["timestamp"].dt.hour]).mean()
    
    return df


df = sentiment_rolling_averages(countries = ['England', 'Wales', 'Iceland'], interval = 'hour')
print(df)

output_file("timeseries.html")

# Plot sentiment against time, use the countries to colour the series lines.
p = TimeSeries(df, x='timestamp', y='sentiment', color='country', width=1200)

show(p)
