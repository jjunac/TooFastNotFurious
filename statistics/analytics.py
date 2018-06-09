from simulator import Exit
from statistics.report_generator import create_graphic_report_average_car_per_exit


class Analytics:

    def __init__(self, nodes):
        self.nodes = nodes

    def get_path_with_their_exit_nodes(self):
        stats = {}
        exit_nodes = [n for n in self.nodes if type(n) is Exit]
        for node in exit_nodes:
            stats[node] = node.get_cars_arrived()

        return stats

    def generate_report(self):
        cars = self.get_path_with_their_exit_nodes()

        res = self.compute_function_per_exit(self.compute_average, cars)
        create_graphic_report_average_car_per_exit(res)

    @staticmethod
    def compute_function_per_exit(fct, cars):
        result = {}

        for key, value in cars.items():
            path = {}

            for entry, val in value.items():
                if not entry[0] in path:
                    path[entry[0]] = []

                for i in range(len(val)):
                    path[entry[0]].append(len(val[i]))

            fct(path)

            result[key] = path

        return result

    @staticmethod
    def compute_average(average):

        for entry, val in average.items():
            average[entry] = sum(val) / len(val)
