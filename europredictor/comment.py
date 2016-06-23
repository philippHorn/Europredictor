# -*- coding: utf-8 -*-
from .keywords import keywords
import re

class Comment(object):
	"""
	Takes a Comment praw object
	"""
	def __init__(self, comment):
		self.body = comment.body.encode('utf-8')
		self.url = comment.permalink
		self.username = comment.author.name
		self.flair = comment.author_flair_text
		self.thread_title = comment.link_title
		self.thread_url = comment.link_url
		self.posted = comment.created_utc
		self.countries = self._find_countries()

	def __str__(self):
		return self.body
		
	def _find_countries(self):
		"""find all countries mentioned in the comment"""
		return [country for country, patterns in keywords.items() 
				if any((re.search(pattern, self.body, flags=re.IGNORECASE)
				for pattern in patterns))]