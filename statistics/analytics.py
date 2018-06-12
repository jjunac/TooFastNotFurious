from math import ceil
from collections import Counter

from simulator import Exit, Road, Entry
from statistics.report_generator import create_graphic_report_average_car_per_exit


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

        res_average = self.compute_function_per_exit(self.compute_average, cars)
        res_median = self.compute_function_per_exit(self.compute_median, cars)
        res_first_quartile = self.compute_function_per_exit(self.compute_first_quartile, cars)
        res_third_quartile = self.compute_function_per_exit(self.compute_third_quartile, cars)
        expectancy_load = self.compute_delay_time_expectancy_with_traffic_load(self.compute_delay_time_by_car())
        create_graphic_report_average_car_per_exit(res_average, res_median, res_first_quartile, res_third_quartile,
                                                   self.traffic_load, expectancy_load)

    @staticmethod
    def compute_function_per_exit(fct, cars):
        result = {}

        for key, value in cars.items():
            path_lengths = {}

            for entry, val in value.items():
                if not entry[0] in path_lengths:
                    path_lengths[entry[0]] = []
                # print(val)
                for i in range(len(val)):
                    path_lengths[entry[0]].append(len(val[i].visited_nodes))
                    path_lengths[entry[0]].sort()

            fct(path_lengths)

            result[key] = path_lengths

        return result

    @staticmethod
    def compute_average(path_lengths):
        for entry, val in path_lengths.items():
            path_lengths[entry] = sum(val) / len(val)

    @staticmethod
    def compute_first_quartile(path_lengths):
        for entry, val in path_lengths.items():
            path_lengths[entry] = val[(ceil(len(val) / 4)) - 1]

    @staticmethod
    def compute_third_quartile(path_lengths):
        for entry, val in path_lengths.items():
            path_lengths[entry] = val[(ceil((3 * len(val)) / 4)) - 1]

    @staticmethod
    def compute_median(path_lengths):
        for entry, val in path_lengths.items():
            if len(val) % 2:
                path_lengths[entry] = val[(ceil((len(val)) / 2)) - 1]
            else:
                index = len(val) / 2
                path_lengths[entry] = (val[int(index) - 1] + val[int(index)]) / 2

    def compute_delay_time_by_car(self):
        nodes = self.get_path_with_their_exit_nodes()
        delay = {}

        for value in nodes.values():

            for val in value.values():

                for i in range(len(val)):
                    if len(val[i].visited_nodes) - len(val[i].original_path.nodes) != 0:
                        if not val[i] in delay:
                            delay[val[i]] = len(val[i].visited_nodes) - len(val[i].original_path.nodes)

        # print(delay)

        return delay

    def compute_delay_time_expectancy_with_traffic_load(self, delay):

        graph = {}

        for i in range(len(self.traffic_load)):
            for key, value in delay.items():
                if key.departure_tick <= i <= key.departure_tick + len(key.visited_nodes):
                    if not i in graph:
                        graph[i] = []
                    graph[i].append(value)

        # print(graph)

        esperance = {}

        for entry, val in graph.items():

            proba = 0

            for key, value in dict(Counter(val)).items():
                proba += (key * key) * (value / len(val))

            if not entry in esperance:
                esperance[entry] = proba

        return esperance
