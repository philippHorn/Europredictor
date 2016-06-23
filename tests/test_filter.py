import unittest
from europredictor.filter import filter_by_body
from europredictor.comment import Comment

class SimpleComment(Comment):
    """simplified comment class for testing"""
    def __init__(self, body):
        self.body = body
        self.countries = self._find_countries()

class FilterTestCase(unittest.TestCase):

    def setUp(self):
        self.one_country = ["Ireland played well", "North Ireland played bad", "germany was ok", "well played france", "Belgian players play well"]
        self.no_country = ["Hello", "This is a comment", ""]
        self.mult_country = ["Ireland is better than N. Ireland", "France and England both did well", "wales did better than turkey", "The Swiss played better than the Italian"]
        self.all_comments = [SimpleComment(body) for body in self.one_country + self.no_country + self.mult_country]

    def test_one_country(self):
        result = filter_by_body(self.all_comments)[0]
        self.assertEqual([r.body for r in result], self.one_country)

    def test_mult_country(self):
        result = filter_by_body(self.all_comments)[1]
        self.assertEqual([r.body for r in result], self.mult_country)