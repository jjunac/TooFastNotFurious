import unittest

from simulator import EntryNode, Path, ExitNode
from statistics import *


class TestAverage(unittest.TestCase):

    def test_average(self):
        entry1 = EntryNode(1, 0)
        entry2 = EntryNode(1, 0)
        entry3 = EntryNode(1, 0)

        p1 = Path([0] * 6)
        p2 = Path([0] * 8)

        exit1 = ExitNode()
        exit2 = ExitNode()

        stats = {exit1: {(entry1, p1): [6, 8, 5, 9], (entry2, p2): [8, 4, 6, 23, 7]},
                 exit2: {(entry3, p1): [5, 6, 5, 7, 2], (entry3, p2): [8, 7, 4, 56, 6, 7]}}

        res = compute_average_per_exit(stats)

        self.assertEqual({exit1: {entry1: 7.0, entry2: 9.6}, exit2: {entry3: 10.272727272727273}}, res)

