import pandas as pd


def prep(path):
    df = pd.read_csv(path, sep='\t')
    temp = df.iloc[:, 0]
    u = df.iloc[:, 1]
    return temp, u


def data_generator(index, path):
    x, y = prep(path)
    if index < len(x):
        return [x[index], y[index]]
    else:
        return False
