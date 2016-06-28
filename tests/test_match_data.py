import unittest
from datetime import datetime
from europredictor.match_data import get_all_matches, Match, get_future_matches


class FilterTestCase(unittest.TestCase):

    def test_all_matches(self):
        matches = get_all_matches()
        self.assertIsInstance(matches[0], Match)
        
        
    def test_future_matches(self):
        matches = get_future_matches()
        self.assertTrue(all([match.start_date > datetime.now() for match in matches]))