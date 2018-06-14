from jinja2 import Environment, PackageLoader, select_autoescape

import datetime


def create_graphic_report(stats, traffic_load,
                          expectancy_load, consumption):
    env = Environment(
        loader=PackageLoader('analytic', 'templates'),
        autoescape=select_autoescape(['html'])
    )

    explored_entry = {}
    explored_exit = {}

    entry_name = "entry"
    exit_name = "exit"

    index_entry = 1
    index_exit = 1

    stats_string_average = create_state_string(stats[0], entry_name, exit_name, explored_entry, explored_exit,
                                               index_entry, index_exit)
    stats_string_first_q = create_state_string(stats[1], entry_name, exit_name, explored_entry, explored_exit,
                                               index_entry, index_exit)
    stats_string_median = create_state_string(stats[2], entry_name, exit_name, explored_entry, explored_exit,
                                              index_entry, index_exit)
    stats_string_third_q = create_state_string(stats[3], entry_name, exit_name, explored_entry, explored_exit,
                                               index_entry, index_exit)

    dataset_average = []
    dataset_median = []
    dataset_first_q = []
    dataset_third_q = []
    labels = []

    for key, value in stats_string_average.items():

        for entry, val in value.items():
            dataset_average.append(val)
            labels.append(key + " - " + entry)

    fill_dataset(dataset_median, stats_string_median)
    fill_dataset(dataset_first_q, stats_string_first_q)
    fill_dataset(dataset_third_q, stats_string_third_q)

    data_traffic_load = []
    data_delay_time = []

    data_average_consumption = []
    data_first_q_consumption = []
    data_median_consumption = []
    data_third_q_consumption = []

    for i in range(len(traffic_load)):
        data_traffic_load.append({'x': i, 'y': traffic_load[i]})
        if i in expectancy_load:
            data_delay_time.append({'x': i, 'y': expectancy_load[i]})
        if i in consumption[0]:
            data_average_consumption.append({'x': i, 'y': consumption[0][i]})
            data_first_q_consumption.append({'x': i, 'y': consumption[1][i]})
            data_median_consumption.append({'x': i, 'y': consumption[2][i]})
            data_third_q_consumption.append({'x': i, 'y': consumption[3][i]})

    template = env.get_template('template_report.html')

    now = datetime.datetime.now()

    name = "report_" + now.strftime("%Y_%m_%d_%Hh%Mm%S") + ".html"

    with open(name, 'w+') as file:
        file.write(template.render(labels=labels, data_average=dataset_average, data_median=dataset_median,
                                   data_first_q=dataset_first_q, data_third_q=dataset_third_q,
                                   data_traffic_load=data_traffic_load, data_delay_time=data_delay_time,
                                   data_average_consumption=data_average_consumption,
                                   data_first_q_consumption=data_first_q_consumption,
                                   data_median_consumption=data_median_consumption,
                                   data_third_q_consumption=data_third_q_consumption))


def fill_dataset(dataset, stats_string):
    for key, value in stats_string.items():

        for entry, val in value.items():
            dataset.append(val)


def create_state_string(stats, entry_name, exit_name, explored_entry, explored_exit, index_entry,
                        index_exit):
    stats_string = {}

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

    return stats_string
