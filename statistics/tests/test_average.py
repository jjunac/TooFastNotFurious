import unittest

from statistics.average import compute_average_per_exit
from simulator import Path, Simulator, Entry, Exit
from statistics.report_generator import create_graphic_report_average_car_per_exit


class TestAverage(unittest.TestCase):

    def test_average(self):
        s = Simulator()
        entry1 = Entry(s, 0, 1)
        entry2 = Entry(s, 0, 1)
        entry3 = Entry(s, 0, 1)

        p1 = Path([0] * 6)
        p2 = Path([0] * 8)

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        stats = {exit1: {(entry1, p1): [6, 8, 5, 9], (entry2, p2): [8, 4, 6, 23, 7]},
                 exit2: {(entry3, p1): [5, 6, 5, 7, 2], (entry3, p2): [8, 7, 4, 56, 6, 7]}}

        res = compute_average_per_exit(stats)

        self.assertEqual({exit1: {entry1: 7.0, entry2: 9.6}, exit2: {entry3: 10.272727272727273}}, res)


if __name__ == '__main__':
    unittest.main()
