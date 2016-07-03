# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
from datetime import datetime
from datetime import datetime
from copy import deepcopy
from settings import DATABASE_NAME
from keywords import keywords

def set_up_db():
    sql = "INSERT INTO countries (name) VALUES (?)"
    conn = _connect_db(DATABASE_NAME)
    cursor = conn.cursor()
    
    for country in keywords:
        print country
        cursor.execute(sql, (country, ))
    conn.commit()

def store_analysed_comment(analysed_comment, overwrite = False):
    '''
    Stores an analysed comment in the db. 
    If the comment has multiple countrys then a database entry will be made for each one.
    Calls _safe_write to check if comment exists in db and perform writing.

    :param analysed_comment: comment
    :param overwrite: Bool
    :return:
    '''
    
    if len(analysed_comment.countries) == 0:
        raise ValueError()
        
    elif len(analysed_comment.countries) == 1:
        _safe_write(analysed_comment, overwrite)
        return
    
    else:
        for country in analysed_comment.countries:
            comment_copy = deepcopy(analysed_comment)
            comment_copy.countries = [country]
            _safe_write(comment_copy, overwrite)
        return


def _safe_write(analysed_comment, overwrite = False):
    '''
    Checks if a (single country) comment exists already in the db.
    Will not overwrite exisiting db entry unless overwrite explicitly set.

    :param analysed_comment: comment
    :param overwrite: Bool
    :return:
    '''
    
    if _comment_exists(analysed_comment) and (overwrite == False):
        print("Comment already exists in db, will not overwrite")
        return
    elif _comment_exists(analysed_comment) and (overwrite == True):
        print("Comment already exists but will be overwritten")
        _write_comment_to_db(analysed_comment)
        return
    else:
        print("Comment does not already exist, writing to db")
        _write_comment_to_db(analysed_comment)
        return
            

def _connect_db(db_name):
    '''
    Setup db connection.

    :param db_name: string
    :return: sqlite connection
    '''

    return sqlite3.connect(db_name)


def _comment_exists(comment):
    '''
    Checks if comment already exists in db.

    :param comment: comment
    :return: Bool
    '''

    conn = _connect_db(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT comments.id FROM comments JOIN countries 
        WHERE comments.country = countries.id
        AND comments.comment LIKE ?
        AND countries.name LIKE ?
        """, (comment.body, comment.countries[0]))

    return bool(cursor.fetchone())

def find_oldest():
    conn = _connect_db(DATABASE_NAME)
    timestamp_cur = conn.execute("SELECT timestamp FROM comments ORDER BY timestamp ASC")
    timestamp = timestamp_cur.fetchone()[0]
    print "Oldest timestamp: ", datetime.fromtimestamp(timestamp)
    return timestamp

def _write_comment_to_db(analysed_comment):
    '''
    Directly writes a comment to the db.

    :param analysed_comment: comment
    :return: None
    '''
    conn = _connect_db(DATABASE_NAME)
    country_id = conn.execute("SELECT id FROM countries WHERE name = ?", 
                               (analysed_comment.countries[0], ))
    sql = "INSERT INTO comments \
            (timestamp, comment, flair, score, country, pos_sentiment, neg_sentiment) \
            VALUES (:timestamp, :comment, :flair, :score, :country, :pos_s, :neg_s)"
    params = {
        "flair"    : analysed_comment.flair,
        "score"    : analysed_comment.score,
        "timestamp": analysed_comment.posted,
        "comment"  : analysed_comment.body,
        "country"  : country_id.fetchone()[0],
        "pos_s"    : analysed_comment.polarity_scores['pos'],
        "neg_s"    : analysed_comment.polarity_scores['neg'],
        }
    
    conn.execute(sql, params)
    conn.commit()
    print('Comment successfully written to db')
    """except:
        with open("error.txt", "wb") as file:
            file.write(str(params))
            print params"""

def read_to_dataframe(countries = None, average = False, start_time = 0, end_time = datetime.now()):
    '''



    '''
    # If no contires specified, retrieve all comments
    if countries == None:
        
        sql_params = (start_time, end_time)
        if average == False:
            sql_query = 'SELECT * FROM comments WHERE timestamp >= ?  AND timestamp < ? ORDER BY timestamp DESC'
        elif average == True:
            sql_query = 'SELECT country, avg(pos_sentiment), avg(neg_sentiment) FROM comments \
            WHERE timestamp >= ?  AND timestamp < ? GROUP by country'
        else:
            raise ValueError()
            
    else:
        
        placeholders = ", ".join("?" * len(countries))
        sql_params = [start_time, end_time]
        sql_params.extend(countries)
        if average == False: 
            sql_query = 'SELECT name, timestamp, pos_sentiment, neg_sentiment FROM comments JOIN countries WHERE comments.country = countries.id AND comments.timestamp >= ?  AND comments.timestamp < ? AND countries.name IN (%s) ORDER BY timestamp DESC' % placeholders
        elif average == True:
            sql_query = 'SELECT country, avg(pos_sentiment), avg(neu_sentiment), avg(neg_sentiment), avg(comp_sentiment) FROM comments \
            WHERE timestamp >= ?  AND timestamp < ? AND country IN (%s) GROUP by country ORDER BY timestamp DESC' % placeholders 
        else:
            raise ValueError()

    conn = _connect_db(DATABASE_NAME)
    df = pd.read_sql_query(sql_query, conn, params = sql_params)
    return df