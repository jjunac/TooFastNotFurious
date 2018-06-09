def compute_function_per_exit(fct, cars):
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


def compute_average(average):
    for entry, val in average.items():
        average[entry] = sum(val) / len(val)
