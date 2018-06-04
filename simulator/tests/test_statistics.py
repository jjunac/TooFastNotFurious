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

        stat.add_travel_time(entry2, 200)
        stat.add_travel_time(entry2, 400)
        stat.add_travel_time(entry2, 400)
        stat.add_travel_time(entry2, 800)

        stat.add_travel_time(entry3, 600)
        stat.add_travel_time(entry3, 800)
        stat.add_travel_time(entry3, 1000)

        average = stat.compute_average(entry1, 2)
        self.assertIsNotNone(stat.list_time_travel[entry1])
        self.assertEqual(150, average)
        self.assertNotEqual(800, average)
        self.assertNotEqual(450, average)

        average = stat.compute_average(entry2, 4)
        self.assertIsNotNone(stat.list_time_travel[entry2])
        self.assertEqual(450, average)
        self.assertNotEqual(800, average)
        self.assertNotEqual(150, average)

        self.assertIsNotNone(stat.list_time_travel[entry3])
        average = stat.compute_average(entry3, 3)
        self.assertEqual(800, average)
        self.assertNotEqual(150, average)
        self.assertNotEqual(450, average)
