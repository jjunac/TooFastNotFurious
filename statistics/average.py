def compute_average_per_exit(stats):
    result = {}

    for key, value in stats.items():
        average = {}

        for entry, val in value.items():
            if not entry[0] in average:
                average[entry[0]] = []

            average[entry[0]] += val

        for entry, val in average.items():
            print(entry)
            average[entry] = sum(val) / len(val)

        result[key] = average

    return result
