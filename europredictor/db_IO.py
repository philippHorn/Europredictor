import sqlite3
from copy import deepcopy
from settings import DATABASE_NAME


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
        SELECT id FROM comments WHERE
        'thread_url' LIKE '{}' AND 'comment_url' LIKE '{}'
        AND 'country' LIKE '{}'
        """.format(comment.thread_url, comment.url, comment.countries[0]))
    if cursor.fetchone():
        return True
    else:
        return False


def _write_comment_to_db(analysed_comment):
    '''
    Directly writes a comment to the db.

    :param analysed_comment: comment
    :return: None
    '''
    conn = _connect_db(DATABASE_NAME)
    sql = "INSERT INTO comments \
            (thread_url, thread_title, comment_url, timestamp, username, comment, country, pos_sentiment, neu_sentiment, neg_sentiment, comp_sentiment) \
            VALUES (:t_url, :t_title, :c_url, :timestamp, :username, :comment, :country, :pos_s, :neu_s, :neg_s, :comp_s)"
    params = {
        "t_url"    : analysed_comment.thread_url,
        "t_title"  : analysed_comment.thread_title,
        "c_url"    : analysed_comment.url,
        "timestamp": analysed_comment.posted,
        "username" : analysed_comment.username,
        "comment"  : analysed_comment.body,
        "country"  : analysed_comment.countries[0],
        "pos_s"    : analysed_comment.polarity_scores['pos'],
        "neu_s"    : analysed_comment.polarity_scores['neu'],
        "neg_s"    : analysed_comment.polarity_scores['neg'],
        "comp_s"   : analysed_comment.polarity_scores['compound']
        }
    try:
        conn.execute(sql, params)
        conn.commit()
        print('Comment successfully written to db')
    except:
        with open("error.txt", "wb") as file:
            file.write(str(params))
            print params
    return