from unittest import TestCase
from nanda import distance


class TestDistance(TestCase):
    def test_distance(self):
        self.assertEqual(distance((0, 0), (1, 1)), 2 ** 0.5)
