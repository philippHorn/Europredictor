from comment import Comment, get_all_comments, split_to_country
from db_IO import store_analysed_comment
#from apscheduler.schedulers.blocking import BlockingScheduler


#sched = BlockingScheduler()



#@sched.scheduled_job('interval', hours=1)
def run_all(time_interval, comment_limit=None):

    comments = get_all_comments(time_interval, comment_limit)
    
    for comment in comments:
        if len(comment.countries) == 1:
            comment.analyse()
            store_analysed_comment(comment, overwrite = False)
        elif len(comment.countries) > 1:
            individual_country = split_to_country(comment)
            for comment in individual_country:
                comment.analyse()
                store_analysed_comment(comment, overwrite = False)
    print "Done"
    """
    Logic goes here
    
    """

run_all("hours")
# sched.start()
