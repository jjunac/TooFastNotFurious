from jinja2 import Environment, PackageLoader, select_autoescape
from random import randrange

from simulator import EntryNode, Path, ExitNode

env = Environment(
    loader=PackageLoader('statistics', 'templates'),
    autoescape=select_autoescape(['html'])
)

entry1 = EntryNode(1, 0)
entry2 = EntryNode(1, 0)
entry3 = EntryNode(1, 0)

p1 = Path([0] * 6)
p2 = Path([0] * 8)

exit1 = ExitNode()
exit2 = ExitNode()

stats = {exit1: {entry1: 7.0, entry2: 9.6}, exit2: {entry3: 10.27}}

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

print(list(stats_string.keys()))

template = env.get_template('bar_chart_template.html')

print(template.render(labels=labels, data=dataset, backgroundColor=background_color))

