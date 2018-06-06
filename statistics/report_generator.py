from jinja2 import Environment, PackageLoader, select_autoescape
from random import randrange

import datetime


def create_graphic_report_average_car_per_exit(stats):
    env = Environment(
        loader=PackageLoader('statistics', 'templates'),
        autoescape=select_autoescape(['html'])
    )

    stats_string = {}

    explored_entry = {}
    explored_exit = {}

    entry_name = "entry"
    exit_name = "exit"

    index_entry = 1
    index_exit = 1

    for key, value in stats.items():

        # if not key.__hash__() in explored_exit:
        #     explored_exit[key.__hash__()] = exit_name + str(index_exit)
        #     index_exit += 1
        key_exit = exit_name + str(index_exit)
        if not key_exit in stats_string:
            stats_string[key_exit] = {}

        for entry, val in value.items():

            # if not entry.__hash__() in explored_entry:
            #     explored_entry[entry.__hash__()] = entry_name + str(index_entry)

            key_entry = entry_name + str(index_entry)
            if not key_entry in stats_string[key_exit]:
                stats_string[key_exit][key_entry] = {}
                stats_string[key_exit][key_entry] = val
            index_entry += 1
            print(entry.__hash__())
        index_exit += 1

    dataset = []
    background_color = []
    labels = []

    for key, value in stats_string.items():

        for entry, val in value.items():
            background_color.append("rgba(" + str(randrange(255)) + ", " + str(
                randrange(255)) + ", " + str(randrange(255)) + ", 0.7)")
            dataset.append(val)
            labels.append(key + " - " + entry)

    template = env.get_template('bar_chart_average_template.html')

    now = datetime.datetime.now()

    name = "report_" + now.strftime("%Y_%m_%d_%Hh%M") + ".html"

    with open(name, 'w+') as file:
        file.write(template.render(labels=labels, data=dataset, backgroundColor=background_color))
