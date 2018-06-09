import unittest

from shared import Orientation
from simulator import Path, Simulator, Entry, Exit, Road
from statistics.analytics import Analytics
from statistics.report_generator import create_graphic_report_average_car_per_exit

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

        p1 = Path([0] * 6)
        p2 = Path([0] * 8)

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        a = Analytics({})

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][0])

        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][0])

        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][0])

        stats = {
            exit1: {(entry1, p1): [nodes, nodes, nodes, nodes, nodes], (entry2, p2): [nodes, nodes1, nodes1, nodes1]},
            exit2: {(entry3, p1): [nodes1, nodes, nodes2, nodes2],
                    (entry3, p2): [nodes2, nodes2, nodes2, nodes, nodes1]}}

        res_a = a.compute_function_per_exit(a.compute_average, stats)
        res_m = a.compute_function_per_exit(a.compute_median, stats)
        res_first_q = a.compute_function_per_exit(a.compute_median, stats)
        res_third_q = a.compute_function_per_exit(a.compute_median, stats)

        create_graphic_report_average_car_per_exit(res_a, res_m, res_first_q, res_third_q)

        now = datetime.datetime.now()

        name = "report_" + now.strftime("%Y_%m_%d_%Hh%Mm%S") + ".html"

        p = P('.')

        self.assertEqual(name, list(p.glob('./' + name))[0].name)

        parser = ParserHTML()

        parser.feed(list(p.glob('./*.html'))[0].read_text())

        script = parser.scripts[3]

        script = re.search(r'var data_average = .*$', script, re.DOTALL).group()

        script = script.replace('var data_average =', '')

        j = json.loads(
            demjson.encode(demjson.decode(script.replace('var AverageChart = new Chart(average_chart, data_average);', ''))))

        labels_expected = ['exit1 - entry1', 'exit1 - entry2', 'exit2 - entry3']
        data_expected = [10, 17.5, 23.333333333333332]
        pattern = 'rgba\([1-2]?[0-9]?[0-9], [1-2]?[0-9]?[0-9], [1-2]?[0-9]?[0-9], 0.7\)'

        for i in range(len(j['data']['labels'])):
            self.assertTrue(labels_expected[i] in j['data']['labels'])
            self.assertTrue(data_expected[i] in j['data']['datasets'][0]['data'])
            self.assertRegex(j['data']['datasets'][0]['backgroundColor'][i], pattern)

        list(p.glob('./' + name))[0].unlink()


class ParserHTML(HTMLParser):

    def error(self, message):
        pass

    def __init__(self):
        super().__init__()
        self.tag = ""
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        self.tag = tag

    def handle_data(self, data):
        if self.tag == "script":
            self.scripts.append(data)


if __name__ == '__main__':
    unittest.main()
