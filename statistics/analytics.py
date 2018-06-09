from simulator import Exit
from statistics.average import *
from statistics.report_generator import create_graphic_report_average_car_per_exit


class Analytics:

    def __init__(self, nodes):
        self.nodes = nodes
        self.functions = {"average": self.compute_average}

    def get_stats_exit_nodes(self):
        stats = {}
        exit_nodes = [n for n in self.nodes if type(n) is Exit]
        for node in exit_nodes:
            stats[node] = node.get_cars_arrived()

        return stats

    def generate_report_average(self):
        cars = self.get_stats_exit_nodes()
        res = compute_function_per_exit(compute_average, cars)
        create_graphic_report_average_car_per_exit(res)

    def compute_function_per_exit(self, fct, cars):
        result = {}

        for key, value in cars.items():
            average = {}

            for entry, val in value.items():
                if not entry[0] in average:
                    average[entry[0]] = []

                for i in range(len(val)):
                    average[entry[0]].append(len(val[i]))

            fct(average)

            result[key] = average

        return result

    def compute_average(self, average):
        for entry, val in average.items():
            average[entry] = sum(val) / len(val)

