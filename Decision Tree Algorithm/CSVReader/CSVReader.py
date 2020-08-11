import pandas


def read(filename):
    df = pandas.read_csv(filename, delimiter=",")
    training_data = [list(row) for row in df.values]
    headers = []
    for key in df.keys():
        headers.append(str(key))
    return headers, training_data


def get_dataframe(filename):
    df = pandas.read_csv(filename, delimiter=",")
    return df


def read_without_headers(filename):
    df = pandas.read_csv(filename)
    data = [list(row) for row in df.values]
    return data