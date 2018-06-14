from math import ceil
from collections import Counter
from statistics import mean, median

from simulator import Exit
from analytic.report_generator import create_graphic_report_average_car_per_exit


class Analytics:

    def __init__(self, nodes, traffic_load):
        self.nodes = nodes
        self.traffic_load = traffic_load

    def get_path_with_their_exit_nodes(self):
        stats = {}
        exit_nodes = [n for n in self.nodes if type(n) is Exit]
        for node in exit_nodes:
            stats[node] = node.get_cars_arrived()

        return stats

    def generate_report(self):
        cars = self.get_path_with_their_exit_nodes()

        res = self.compute_function_per_exit(cars)

        consumption = self.compute_consumption_by_car_with_traffic_load(self.compute_consumption_by_car(cars))

        expectancy_load = self.compute_delay_time_expectancy_with_traffic_load(self.compute_delay_time_by_car(cars))
        create_graphic_report_average_car_per_exit(res[0], res[1], res[2], res[3],
                                                   self.traffic_load, expectancy_load, consumption)

    def compute_function_per_exit(self, cars):

        result_a = {}
        result_m = {}
        result_fq = {}
        result_tq = {}

        for key, value in cars.items():
            path_lengths = {}

            average = {}
            med = {}
            first_q = {}
            third_q = {}

            for entry, val in value.items():
                if not entry[0] in path_lengths:
                    path_lengths[entry[0]] = []

                for i in range(len(val)):
                    path_lengths[entry[0]].append(len(val[i].visited_nodes))
                    path_lengths[entry[0]].sort()

            for entry, val in path_lengths.items():
                average[entry] = mean(val)
                med[entry] = median(val)
                first_q[entry] = self.__first_quartile(val)
                third_q[entry] = self.__third_quartile(val)

            result_a[key] = average
            result_m[key] = med
            result_fq[key] = first_q
            result_tq[key] = third_q

        return result_a, result_fq, result_m, result_tq

    def __first_quartile(self, val):
        return val[(ceil(len(val) / 4)) - 1]

    def __third_quartile(self, val):
        return val[(ceil((3 * len(val)) / 4)) - 1]

    def compute_delay_time_by_car(self, nodes):

        delay = {}

        for value in nodes.values():

            for val in value.values():

                for i in range(len(val)):
                    if len(val[i].visited_nodes) - len(val[i].original_path.nodes) != 0 and not val[i] in delay:
                        delay[val[i]] = len(val[i].visited_nodes) - len(val[i].original_path.nodes)

        return delay

    def compute_delay_time_expectancy_with_traffic_load(self, delay):

        graph = {}

        for i in range(len(self.traffic_load)):
            for key, value in delay.items():
                if key.departure_tick <= i <= key.departure_tick + len(key.visited_nodes):
                    if not i in graph:
                        graph[i] = []
                    graph[i].append(value)

        expectancy = {}

        for entry, val in graph.items():

            proba = 0

            for key, value in dict(Counter(val)).items():
                proba += (key * key) * (value / len(val))

            if not entry in expectancy:
                expectancy[entry] = proba

        return expectancy

    def __consumption_function(self, v0, v1):
        return 2 * v1 + v0

    def compute_consumption_by_car(self, nodes):
        conso = {}
        for value in nodes.values():
            for val in value.values():
                for i in range(len(val)):
                    v0 = len(val[i].visited_nodes) - len(val[i].original_path.nodes)
                    v1 = len(val[i].original_path.nodes)
                    conso[val[i]] = self.__consumption_function(v0, v1)
        return conso

    def compute_consumption_by_car_with_traffic_load(self, consumption):

        graph = {}

        for i in range(len(self.traffic_load)):
            for key, value in consumption.items():
                if key.departure_tick <= i <= key.departure_tick + len(key.visited_nodes):
                    if not i in graph:
                        graph[i] = []
                    graph[i].append(value)

        result_a = {}
        result_m = {}
        result_fq = {}
        result_tq = {}

        for entry, val in graph.items():

            val.sort()
            result_a[entry] = mean(val)
            result_m[entry] = median(val)
            result_fq[entry] = self.first_quartile(val)
            result_tq[entry] = self.third_quartile(val)

        return result_a, result_fq, result_m, result_tq
