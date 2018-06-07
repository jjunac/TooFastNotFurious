import unittest

from simulator import *


class TestStatistics(unittest.TestCase):

    def test_add_travel_time(self):
        simulator = Simulator()
        entry1 = Entry(simulator, 0)
        entry2 = Entry(simulator, 0)
        entry3 = Entry(simulator, 0)

        entry1.to_spawn = 0
        entry2.to_spawn = 0
        entry3.to_spawn = 0

        p = Path([])
        p2 = Path([])

        stat = Statistics()

        self.assertFalse(p in stat.list_time_travel)
        self.assertFalse(p2 in stat.list_time_travel)

        stat.add_travel_time(entry1, p, 100)
        stat.add_travel_time(entry1, p, 200)

        stat.add_travel_time(entry1, p2, 600)
        stat.add_travel_time(entry1, p2, 500)
        stat.add_travel_time(entry1, p2, 800)

        self.assertEqual(100, stat.list_time_travel[(entry1, p)][0])
        self.assertEqual(200, stat.list_time_travel[(entry1, p)][1])

        self.assertEqual(600, stat.list_time_travel[(entry1, p2)][0])
        self.assertEqual(500, stat.list_time_travel[(entry1, p2)][1])
        self.assertEqual(800, stat.list_time_travel[(entry1, p2)][2])

        self.assertEqual(2, len(stat.list_time_travel[(entry1, p)]))
        self.assertEqual(3, len(stat.list_time_travel[(entry1, p2)]))
