from praw import Reddit
from comment import Comment
from apscheduler.schedulers.blocking import BlockingScheduler

r = Reddit(user_agent='Get comments from soccer subreddit')
sched = BlockingScheduler()

def get_comments():
	user = r.get_subreddit('soccer')
	comments = user.get_comments(sort='new', time='hour', limit=10)

	return [Comment(c) for c in comments]


@sched.scheduled_job('interval', hours=1)
def run_all():

	comments = get_comments()
	
	"""
	Logic goes here
	"""

run_all()
sched.start()