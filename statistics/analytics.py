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
        create_graphic_report_average_car_per_exit(res_average, res_median, res_first_quartile, res_third_quartile)

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

    def compute_stop_time(self):
        nodes = self.get_path_with_their_exit_nodes()
        roads = {}

        for key, value in nodes.items():
            for entry, val in value.items():
                for i in range(len(val)):
                    c = Counter(val[i].visited_nodes)
                    for k, v in dict(Counter(n for n in c.elements() if c[n] > 1)).items():
                        if not (k.entity, val[i]) in roads:
                            roads[(k.entity, val[i])] = []

                        roads[(k.entity, val[i])].append(v)

        print(roads)

        return roads

        #
        # for i in range(len(self.traffic_load)):
        #     for key, value in roads.items():
        #         if key[1].departure_tick >= i:
        #             print(value)

