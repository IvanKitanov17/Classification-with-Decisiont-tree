from Algorithm.HelperMethods import is_number


class Question:

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def compare(self, other):
        other_value = other[self.column]
        if is_number(other_value):
            return other_value >= self.value
        else:
            return other_value == self.value

    def get_value(self):
        return self.value

    def get_column(self):
        return self.column