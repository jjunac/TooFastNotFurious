from jinja2 import Environment, PackageLoader, select_autoescape
from random import randrange


def create_graphic_report(stats):
    env = Environment(
        loader=PackageLoader('statistics', 'templates'),
        autoescape=select_autoescape(['html'])
    )

    stats_string = {}

    entry_name = "entry"
    exit_name = "exit"

    index_entry = 1
    index_exit = 1

    for key, value in stats.items():

        key_exit = exit_name + str(index_exit)
        if not key_exit in stats_string:
            stats_string[key_exit] = {}

        for entry, val in value.items():
            key_entry = entry_name + str(index_entry)
            if not key_entry in stats_string[key_exit]:
                stats_string[key_exit][key_entry] = {}
                stats_string[key_exit][key_entry] = val
            index_entry += 1

        index_exit += 1

    dataset = []
    background_color = []
    labels = []

    for key, value in stats_string.items():

        for entry, val in value.items():
            background_color.append("rgba(" + str(randrange(255)) + ", " + str(
                randrange(255)) + ", " + str(randrange(255)) + ", 0.2)")
            dataset.append(val)
            labels.append(key + " - " + entry)

    template = env.get_template('bar_chart_template.html')

    with open('../html/report.html', 'w+') as file:
        file.write(template.render(labels=labels, data=dataset, backgroundColor=background_color))
