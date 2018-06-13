import unittest

from shared import Orientation
from simulator import Path, Simulator, Entry, Exit, Road, Car
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

        p1 = Path([])
        p2 = Path([])

        exit1 = Exit(s, 1)
        exit2 = Exit(s, 1)

        road1 = Road(s, 100, Orientation.SOUTH, 1)

        car1 = Car(p2, entry1, 0)
        car2 = Car(p2, entry2, 0)
        car3 = Car(p2, entry3, 0)
        car4 = Car(p2, entry1, 0)
        car5 = Car(p2, entry2, 0)
        car6 = Car(p2, entry3, 0)

        nodes = []

        for i in range(0, 10):
            nodes.append(road1.nodes[0][i])

        car1.visited_nodes = nodes
        car6.visited_nodes = nodes
        nodes1 = []

        for i in range(0, 20):
            nodes1.append(road1.nodes[0][i])

        car2.visited_nodes = nodes1
        car4.visited_nodes = nodes1
        nodes2 = []

        for i in range(0, 30):
            nodes2.append(road1.nodes[0][i])

        car3.visited_nodes = nodes2
        car5.visited_nodes = nodes2

        car1.original_path.nodes = nodes
        car2.original_path.nodes = nodes
        car3.original_path.nodes = nodes
        car4.original_path.nodes = nodes
        car5.original_path.nodes = nodes
        car6.original_path.nodes = nodes

        car1.departure_tick = 1
        car2.departure_tick = 1
        car3.departure_tick = 2
        car4.departure_tick = 3
        car5.departure_tick = 3
        car6.departure_tick = 4

        t_load = []

        for i in range(0, 50):
            t_load.append(0)

        t_load[1] = 2
        t_load[2] = 3
        t_load[3] = 5
        t_load[4] = 6

        for i in range(5, 11):
            t_load[i] = 6

        for i in range(11, 15):
            t_load[i] = 5

        for i in range(15, 21):
            t_load[i] = 4

        for i in range(21, 24):
            t_load[i] = 3

        for i in range(24, 32):
            t_load[i] = 2

        t_load[32] = 1
        t_load[33] = 1

        a = Analytics([], t_load)

        stats = {
            exit1: {(entry1, p1): [car1, car1, car1, car1, car1], (entry2, p2): [car1, car2, car2, car2]},
            exit2: {(entry3, p1): [car2, car1, car3, car3],
                    (entry3, p2): [car3, car3, car3, car1, car2]}}

        res_a = a.compute_function_per_exit(a.compute_average, stats)
        res_m = a.compute_function_per_exit(a.compute_median, stats)
        res_first_q = a.compute_function_per_exit(a.compute_median, stats)
        res_third_q = a.compute_function_per_exit(a.compute_median, stats)

        delay = a.compute_delay_time_by_car(stats)

        res = a.compute_delay_time_expectancy_with_traffic_load(delay)

        create_graphic_report_average_car_per_exit(res_a, res_m, res_first_q, res_third_q, t_load, res)

        now = datetime.datetime.now()

        name = "report_" + now.strftime("%Y_%m_%d_%Hh%Mm%S") + ".html"

        p = P('.')

        self.assertEqual(name, list(p.glob('./' + name))[0].name)

        parser = ParserHTML()

        parser.feed(list(p.glob('./*.html'))[0].read_text())

        script = parser.scripts[5]

        script = re.search(r'var data = .*$', script, re.DOTALL).group()

        script = script.replace('var data =', '')

        j = json.loads(
            demjson.encode(
                demjson.decode(script.replace('var ReportChart = new Chart(reportChart, data);', ''))))

        labels_expected = ['exit1 - entry1', 'exit1 - entry2', 'exit2 - entry3']
        data_average = [10, 17.5, 23.333333333333332]
        data_median = [10, 20.0, 30]
        data_f_q = [10, 20.0, 30]
        data_t_q = [10, 20.0, 30]

        for i in range(len(j['data']['labels'])):
            with self.subTest(i=i):
                self.assertTrue(labels_expected[i] in j['data']['labels'])
                self.assertTrue(data_average[i] in j['data']['datasets'][0]['data'])
                self.assertTrue(data_median[i] in j['data']['datasets'][1]['data'])
                self.assertTrue(data_f_q[i] in j['data']['datasets'][2]['data'])
                self.assertTrue(data_t_q[i] in j['data']['datasets'][3]['data'])

        script = parser.scripts[7]

        script = re.search(r'var data = .*$', script, re.DOTALL).group()

        script = script.replace('var data =', '')

        j = json.loads(
            demjson.encode(
                demjson.decode(script.replace('var TrafficLoad = new Chart(reportChart, data);', ''))))

        self.assertTrue({'x': 1, 'y': 100} in j["data"]["datasets"][0]["data"])
        self.assertTrue({'x': 2, 'y': 250} in j["data"]["datasets"][0]["data"])
        self.assertTrue({'x': 8, 'y': 250} in j["data"]["datasets"][0]["data"])
        self.assertTrue({'x': 28, 'y': 400} in j["data"]["datasets"][0]["data"])

        for i in range(len(t_load)):
            with self.subTest(i=i):
                self.assertTrue({'x':i, 'y':t_load[i]} in j["data"]["datasets"][1]["data"])

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
