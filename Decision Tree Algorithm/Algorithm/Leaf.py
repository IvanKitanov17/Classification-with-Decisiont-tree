from Algorithm.HelperMethods import number_of_occurrences_of_labels


class Leaf:

    def __init__(self, training_data):
        self.result = number_of_occurrences_of_labels(training_data)

    def get_result(self):
        return self.result
