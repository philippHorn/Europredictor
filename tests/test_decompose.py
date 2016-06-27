import unittest
from europredictor.decompose import split_to_country
from europredictor.comment import Comment

class SimpleComment(Comment):
    """simplified comment class for testing"""
    def __init__(self, body):
        self.body = body
        self.countries = self.find_countries()
        
    def __eq__(self, other):
        return self.body == other.body


class ClauseTestCase(unittest.TestCase):

    def test_countires_on_different_sentences(self):
        comment1 = SimpleComment("England is good. Wales is bad.")
        comment2 = SimpleComment("I like France. But I don't like Turkey.")
        self.assertEqual(split_to_country(comment1), [SimpleComment("England is good."), SimpleComment("Wales is bad.")])
        self.assertEqual(split_to_country(comment2), [SimpleComment("I like France."), SimpleComment("But I don't like Turkey.")])
        
    def test_sentences_with_no_countries(self):
        comment1 = SimpleComment("England is good. Wales is bad. This is not a country")
        comment2 = SimpleComment("I like France. I also like snails.")
        self.assertEqual(split_to_country(comment1), [SimpleComment("England is good."), SimpleComment("Wales is bad.")])
        self.assertEqual(split_to_country(comment2), [SimpleComment("I like France.")])
        
        
    def test_subclauses(self):
        clauses = ["Ireland is good but North Ireland is better", "France is nice but so is Italy", "Wales did better than turkey", "The Swiss played better than the Italian"]
        comment = SimpleComment("France is nice but so is Italy")
        comments = split_to_country(comment)
        bodys = [comment.body for comment in comments]
        self.assertEqual(bodys, ["France is nice", "so is Italy"])
        
        
