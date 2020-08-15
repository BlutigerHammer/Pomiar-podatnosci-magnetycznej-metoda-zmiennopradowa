import pandas as pd


def prep(path):
    df = pd.read_csv(path, sep='\t')
    temp = df.iloc[:, 0]
    u = df.iloc[:, 1]
    return temp, u


def data_generator(i):
    path = "data\\dane4.txt"
    x, y = prep(path)
    if i <= len(x) - 2:
        return [x[i], y[i]]
    else:
        return False
