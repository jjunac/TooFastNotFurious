from jinja2 import Environment, PackageLoader, select_autoescape
from random import randrange

import datetime


def create_graphic_report_average_car_per_exit(stats_average, stats_median, stats_first_Q, stats_third_Q):
    env = Environment(
        loader=PackageLoader('statistics', 'templates'),
        autoescape=select_autoescape(['html'])
    )

    explored_entry = {}
    explored_exit = {}

    entry_name = "entry"
    exit_name = "exit"

    index_entry = 1
    index_exit = 1

    stats_string_average = {}
    stats_string_median = {}
    stats_string_first_q = {}
    stats_string_third_q = {}

    create_state_string(stats_average, stats_string_average, entry_name, exit_name, explored_entry, explored_exit,
                        index_entry, index_exit)
    create_state_string(stats_median, stats_string_median, entry_name, exit_name, explored_entry, explored_exit,
                        index_entry, index_exit)
    create_state_string(stats_first_Q, stats_string_first_q, entry_name, exit_name, explored_entry, explored_exit,
                        index_entry, index_exit)
    create_state_string(stats_third_Q, stats_string_third_q, entry_name, exit_name, explored_entry, explored_exit,
                        index_entry, index_exit)

    dataset_average = []
    dataset_median = []
    dataset_first_q = []
    dataset_third_q = []
    background_color = []
    labels = []

    for key, value in stats_string_average.items():

        for entry, val in value.items():
            background_color.append("rgba(" + str(randrange(255)) + ", " + str(
                randrange(255)) + ", " + str(randrange(255)) + ", 0.7)")
            dataset_average.append(val)
            labels.append(key + " - " + entry)

    fill_dataset(dataset_median, stats_string_median)
    fill_dataset(dataset_first_q, stats_string_first_q)
    fill_dataset(dataset_third_q, stats_string_third_q)

    template = env.get_template('bar_chart_average_template.html')

    now = datetime.datetime.now()

    name = "report_" + now.strftime("%Y_%m_%d_%Hh%Mm%S") + ".html"

    with open(name, 'w+') as file:
        file.write(template.render(labels=labels, data_average=dataset_average, data_median=dataset_median,
                                   data_first_q=dataset_first_q, data_third_q=dataset_third_q,
                                   backgroundColor=background_color))


def fill_dataset(dataset, stats_string):
    for key, value in stats_string.items():

        for entry, val in value.items():
            dataset.append(val)


def create_state_string(stats, stats_string, entry_name, exit_name, explored_entry, explored_exit, index_entry,
                        index_exit):
    for key, value in stats.items():

        if not key.__hash__() in explored_exit:
            explored_exit[key.__hash__()] = exit_name + str(index_exit)
            index_exit += 1

        if not explored_exit[key.__hash__()] in stats_string:
            stats_string[explored_exit[key.__hash__()]] = {}

        for entry, val in value.items():

            if not entry.__hash__() in explored_entry:
                explored_entry[entry.__hash__()] = entry_name + str(index_entry)
                index_entry += 1

            if not explored_exit[key.__hash__()] in stats_string[explored_exit[key.__hash__()]]:
                stats_string[explored_exit[key.__hash__()]][explored_entry[entry.__hash__()]] = {}
                stats_string[explored_exit[key.__hash__()]][explored_entry[entry.__hash__()]] = val
