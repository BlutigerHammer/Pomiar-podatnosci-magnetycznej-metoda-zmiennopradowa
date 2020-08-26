import pandas as pd
from pathlib import Path


def save_to_xmls(path, data1, data2, sheet_name):
    str1 = 'pos'
    str2 = 'volt'
    df = pd.DataFrame({str1: data1, str2: data2})
    df.index += 1

    writer = pd.ExcelWriter(path=path, engine="openpyxl", mode='a')
    df.to_excel(writer, sheet_name=sheet_name)
    writer.save()

def create_xmls(path):
    sheet_name = 'setup'
    writer = pd.ExcelWriter(path=path, engine="openpyxl", mode='w')
    df = pd.DataFrame({'Witaj'})
    df.to_excel(writer, sheet_name=sheet_name)
    writer.save()


def save_to_csv(path, data1, data2):
    str1 = 'pos'
    str2 = 'volt'
    df = pd.DataFrame({str1: data1, str2: data2})
    df.to_csv(path_or_buf=path, index=False, sep='\t')


if __name__ == '__main__':
    path = Path('data/excel1.xlsx')
    x = [1, 2, 3, 4, 5, 6, 7]
    y = [11, 12, 13, 14, 15, 16, 17]
    create_xmls(path)
    save_to_xmls(path, x, y, 'arkusz1')

