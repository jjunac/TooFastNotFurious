import unittest

from statistics.average import compute_average_per_exit
from simulator import Path, Simulator, Entry, Exit
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
        entry1 = Entry(s, 0)
        entry2 = Entry(s, 0)
        entry3 = Entry(s, 0)

        p1 = Path([0] * 6)
        p2 = Path([0] * 8)

        exit1 = Exit(s)
        exit2 = Exit(s)

        stats = {exit1: {(entry1, p1): [6, 8, 5, 9], (entry2, p2): [8, 4, 6, 23, 7]},
                 exit2: {(entry3, p1): [5, 6, 5, 7, 2], (entry3, p2): [8, 7, 4, 56, 6, 7]}}

        res = compute_average_per_exit(stats)

        create_graphic_report_average_car_per_exit(res)

        now = datetime.datetime.now()

        name = "report_" + now.strftime("%Y_%m_%d_%Hh%Mm%S") + ".html"

        p = P('.')

        self.assertEqual(name, list(p.glob('./' + name))[0].name)

        parser = ParserHTML()

        parser.feed(list(p.glob('./*.html'))[0].read_text())

        script = parser.scripts[3]

        script = re.search(r'var data = .*$', script, re.DOTALL).group()

        script = script.replace('var data =', '')

        j = json.loads(demjson.encode(demjson.decode(script.replace('var myChart = new Chart(ctx, data);', ''))))

        self.assertEqual(['exit1 - entry1', 'exit1 - entry2', 'exit2 - entry3'], j['data']['labels'])
        self.assertEqual([7.0, 9.6, 10.272727272727273], j['data']['datasets'][0]['data'])
        pattern = 'rgba\([1-2]?[0-9]?[0-9], [1-2]?[0-9]?[0-9], [1-2]?[0-9]?[0-9], 0.7\)'
        self.assertRegex(j['data']['datasets'][0]['backgroundColor'][0], pattern)
        self.assertRegex(j['data']['datasets'][0]['backgroundColor'][1], pattern)
        self.assertRegex(j['data']['datasets'][0]['backgroundColor'][2], pattern)

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
