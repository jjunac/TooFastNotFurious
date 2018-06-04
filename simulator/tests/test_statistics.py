import unittest

from simulator import *


class TestStatistics(unittest.TestCase):

    def test_add_travel_time(self):
        entry1 = EntryNode(1, 0)
        entry2 = EntryNode(1, 0)
        entry3 = EntryNode(1, 0)
        entry1.to_spawn = 0
        entry2.to_spawn = 0
        entry3.to_spawn = 0

        stat = Statistics()

        stat.add_travel_time(entry1, 100)
        stat.add_travel_time(entry1, 200)

        self.assertIsNotNone(stat.list_time_travel[entry1])
        self.assertEqual(150, stat.compute_average(entry1, 2))
