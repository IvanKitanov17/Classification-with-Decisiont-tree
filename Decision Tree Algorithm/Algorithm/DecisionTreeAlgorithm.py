from Algorithm.HelperMethods import number_of_occurrences_of_labels
from Algorithm.Leaf import Leaf
from Algorithm.Question import Question
from Algorithm.SplitNode import SplitNode


def get_unique_values(training_data, col):
    unique_values = set()
    for row in training_data:
        unique_values.add(row[col])
    return unique_values


def split_data(training_data, question):
    true_branch = []
    false_branch = []

    for row in training_data:
        if question.compare(row) == True:
            true_branch.append(row)
        else:
            false_branch.append(row)
    return true_branch, false_branch


def get_gini_impurity(training_data):
    occurences = number_of_occurrences_of_labels(training_data)
    gini_impurity = 1

    for outcome in occurences:
        probability_of_outcome = occurences[outcome] / len(training_data)
        gini_impurity -= probability_of_outcome * probability_of_outcome
    return gini_impurity


def get_information_gain(true_branch, false_branch, gini_impurity):
    weight_of_true_branch = len(true_branch) / (len(true_branch) + len(false_branch))
    return gini_impurity - weight_of_true_branch * get_gini_impurity(true_branch) - (
            1 - weight_of_true_branch) * get_gini_impurity(false_branch)


def get_best_information_gain_question(training_data):
    best_information_gain = 0
    best_question = None
    gini_impurity = get_gini_impurity(training_data)

    for col in range(len(training_data[0]) - 1):
        values = get_unique_values(training_data, col)
        for value in values:
            question = Question(col, value)
            true_rows, false_rows = split_data(training_data, question)

            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            information_gain = get_information_gain(true_rows, false_rows, gini_impurity)

            if information_gain > best_information_gain:
                best_information_gain = information_gain
                best_question = question
    return best_information_gain, best_question


def build_tree(training_data):
    information_gain, question = get_best_information_gain_question(training_data)

    if information_gain == 0:
        return Leaf(training_data)

    true_rows, false_rows = split_data(training_data, question)

    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)

    return SplitNode(question, true_branch, false_branch)


def classify(row, node):
    if isinstance(node, Leaf):
        return node.get_result()

    if node.question.compare(row) == True:
        return classify(row, node.get_true_branch())
    else:
        return classify(row, node.get_false_branch())


def get_results_with_percentages(classificated_row):
    sum_of_values = sum(classificated_row.values())
    result_percentages = {}

    for result in classificated_row.keys():
        percentage = round((classificated_row[result] / sum_of_values * 100.0), 2)
        result_percentages[result] = str(percentage) + "%"
    return result_percentages
