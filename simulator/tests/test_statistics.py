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

        p = Path([0] * 6)
        p2 = Path([0] * 7)

        stat = Statistics()

        self.assertFalse(p in stat.list_time_travel)
        self.assertFalse(p2 in stat.list_time_travel)

        stat.add_travel_time(p, 100)
        stat.add_travel_time(p, 200)

        stat.add_travel_time(p2, 600)
        stat.add_travel_time(p2, 500)
        stat.add_travel_time(p2, 800)

        self.assertEqual(100, stat.list_time_travel[p][0])
        self.assertEqual(200, stat.list_time_travel[p][1])

        self.assertEqual(600, stat.list_time_travel[p2][0])
        self.assertEqual(500, stat.list_time_travel[p2][1])
        self.assertEqual(800, stat.list_time_travel[p2][2])

        self.assertEqual(2, len(stat.list_time_travel[p]))
        self.assertEqual(3, len(stat.list_time_travel[p2]))

