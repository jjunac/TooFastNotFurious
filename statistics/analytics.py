from simulator import Exit
from statistics.average import compute_average_per_exit
from statistics.report_generator import create_graphic_report_average_car_per_exit


class Analytics:

    def __init__(self, nodes):
        self.nodes = nodes

    def get_stats_exit_nodes(self):
        stats = {}
        exit_nodes = [n for n in self.nodes if type(n) is Exit]
        for node in exit_nodes:
            stats[node] = node.get_stats()

        return stats

    def generate_report_average(self):
        stats = self.get_stats_exit_nodes()
        res = compute_average_per_exit(stats)
        create_graphic_report_average_car_per_exit(res)
