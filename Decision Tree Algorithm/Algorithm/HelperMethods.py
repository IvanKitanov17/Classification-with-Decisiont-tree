def number_of_occurrences_of_labels(training_data):
    occurrences = {}

    for row in training_data:
        label = row[-1]
        if label not in occurrences:
            occurrences[label] = 0
        occurrences[label] += 1
    return occurrences


def is_number(parameter):
    if isinstance(parameter, int) or isinstance(parameter, float):
        return True
    return False
