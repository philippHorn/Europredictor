import sqlite3
import nltk

from nltk.sentiment import vader
from settings import DATABASE_NAME


# nltk.download() # must initially download vader_lexicon for vader to work

def analyse(clause):
    '''
    Run the clause through the Vadar polarity scorer and add an attribute to the clause object containing the results

    :param clause: clause
    :return: clause
    '''

    clause.polarity_scores = vader.SentimentIntensityAnalyzer().polarity_scores(clause.body)
    return clause

def store_analysed_clause(analysed_clause, overwrite = False):
    '''
    Stores an analysed clause in the db. If clause already exists will not overwrite unless overwrite param explicity
    set to True.

    :param analysed_clause: clause
    :param overwrite: Bool
    :return:
    '''

    if _clause_exists(analysed_clause) and (overwrite == False):
        print("Clause already exists in db, will not overwrite")
        return
    elif _clause_exists(analysed_clause) and (overwrite == True):
        print("Clause already exists but will be overwritten")
        _write_clause_to_db(analysed_clause)
        return
    else:
        print("Clause does not already exist, writing to db")
        _write_clause_to_db(analysed_clause)
        return

def _connect_db(db_name):
    '''
    Setup db connection.

    :param db_name: string
    :return: sqlite connection
    '''

    return sqlite3.connect(db_name)

def _clause_exists(clause):
    '''
    Checks if clause already exists in db.

    :param clause: clause
    :return: Bool
    '''

    c = _connect_db(DATABASE_NAME)
    cursor = c.cursor()
    cursor.execute(
        "SELECT id FROM clauses WHERE thread_url LIKE'" + \
        clause.thread_url + "' AND comment_url LIKE '" + clause.url + "'")
    if cursor.fetchone():
        return True
    else:
        return False

def _write_clause_to_db(analysed_clause):
    '''
    Directly writes a clause to the db.

    :param analysed_clause: clause
    :return: None
    '''
    c = _connect_db(DATABASE_NAME)
    sql = "INSERT INTO clauses \
            (thread_url, comment_url, timestamp, username, clause, team, pos_sentiment, neu_sentiment, neg_sentiment, comp_sentiment) \
            VALUES (:t_url, :c_url, :timestamp, :username, :clause, :team, :pos_s, :neu_s, :neg_s, :comp_s)"
    params = {
        "t_url"    : analysed_clause.thread_url,
        "c_url"    : analysed_clause.url,
        "timestamp": analysed_clause.posted,
        "username" : analysed_clause.username,
        "clause"   : analysed_clause.body,
        "team"     : analysed_clause.country,
        "pos_s"    : analysed_clause.polarity_scores['pos'],
        "neu_s"    : analysed_clause.polarity_scores['neu'],
        "neg_s"    : analysed_clause.polarity_scores['neg'],
        "comp_s"   : analysed_clause.polarity_scores['compound']
        }

    c.execute(sql, params)
    c.commit()
    return
