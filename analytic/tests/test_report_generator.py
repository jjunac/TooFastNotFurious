import unittest

from shared import Orientation
from simulator import Path, Simulator, Entry, Exit, Road, Car
from analytic.analytics import Analytics
from analytic.report_generator import create_graphic_report_average_car_per_exit, create_state_string

from pathlib import Path as P

import demjson
import json
import re
import datetime

from html.parser import HTMLParser


class TestReportGenerator(unittest.TestCase):

    def test_should_a_correct_report(self):
        s = Simulator()
        entry1 = Entry(s, 0, 1)
        entry2 = Entry(s, 0, 1)
        entry3 = Entry(s, 0, 1)

        p1 = Path([])
        p2 = Path([])

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        car1 = Car(p2, entry1, 0)
        car2 = Car(p2, entry2, 0)
        car3 = Car(p2, entry3, 0)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][i])

        car1.visited_nodes = nodes

        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][i])

        car2.visited_nodes = nodes1

        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][i])

        car3.visited_nodes = nodes2

        car1.departure_tick = 1
        car2.departure_tick = 1
        car3.departure_tick = 2

        a = Analytics([], [])

        stats = {
            exit1: {(entry1, p1): [car1, car1, car1, car1, car1], (entry2, p2): [car1, car2, car2, car2]},
            exit2: {(entry3, p1): [car2, car1, car3, car3],
                    (entry3, p2): [car3, car3, car3, car1, car2]}}

        res_overview = a.compute_function_per_exit(stats)

        explored_entry = {}
        explored_exit = {}

        entry_name = "entry"
        exit_name = "exit"

        index_entry = 1
        index_exit = 1

        string_average = create_state_string(res_overview[0], entry_name, exit_name, explored_entry, explored_exit,
                                             index_entry, index_exit)
        string_f_q = create_state_string(res_overview[1], entry_name, exit_name, explored_entry, explored_exit,
                                         index_entry, index_exit)
        string_median = create_state_string(res_overview[2], entry_name, exit_name, explored_entry, explored_exit,
                                            index_entry, index_exit)
        string_t_q = create_state_string(res_overview[3], entry_name, exit_name, explored_entry, explored_exit,
                                         index_entry, index_exit)

        self.assertTrue('exit1' in string_average)
        self.assertTrue('entry1' in string_average['exit1'])
        self.assertTrue('entry2' in string_average['exit1'])
        self.assertEqual(10, string_average['exit1']['entry1'])
        self.assertEqual(17.5, string_average['exit1']['entry2'])
        self.assertTrue('exit2' in string_average)
        self.assertTrue('entry3' in string_average['exit2'])
        self.assertAlmostEqual(23.3, string_average['exit2']['entry3'], delta=0.1)

        self.assertTrue('exit1' in string_f_q)
        self.assertTrue('entry1' in string_f_q['exit1'])
        self.assertTrue('entry2' in string_f_q['exit1'])
        self.assertEqual(10, string_f_q['exit1']['entry1'])
        self.assertEqual(10, string_f_q['exit1']['entry2'])
        self.assertTrue('exit2' in string_f_q)
        self.assertTrue('entry3' in string_f_q['exit2'])
        self.assertEqual(20, string_f_q['exit2']['entry3'])

        self.assertTrue('exit1' in string_median)
        self.assertTrue('entry1' in string_median['exit1'])
        self.assertTrue('entry2' in string_median['exit1'])
        self.assertEqual(10, string_median['exit1']['entry1'])
        self.assertEqual(20, string_median['exit1']['entry2'])
        self.assertTrue('exit2' in string_median)
        self.assertTrue('entry3' in string_median['exit2'])
        self.assertEqual(30, string_median['exit2']['entry3'])

        self.assertTrue('exit1' in string_t_q)
        self.assertTrue('entry1' in string_t_q['exit1'])
        self.assertTrue('entry2' in string_t_q['exit1'])
        self.assertEqual(10, string_t_q['exit1']['entry1'])
        self.assertEqual(20, string_t_q['exit1']['entry2'])
        self.assertTrue('exit2' in string_t_q)
        self.assertTrue('entry3' in string_t_q['exit2'])
        self.assertEqual(30, string_t_q['exit2']['entry3'])


if __name__ == '__main__':
    unittest.main()
