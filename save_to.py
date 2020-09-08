import pandas as pd
from pathlib import Path


def save_to_csv(path, parameters, x, y):
    # print(data)
    str1 = parameters.get('wartości x')
    str2 = parameters.get('wartości y')
    parameters = pd.DataFrame.from_dict(parameters, orient="index")
    parameters = parameters.transpose()
    parameters.to_csv(path_or_buf=path, index=False, sep='\t', mode='w')
    df = pd.DataFrame({str1: x, str2: y})
    df.to_csv(path_or_buf=path, index=False, sep='\t', mode='a')

def csv_to_xlsx(excel_path, csv_paths):
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
    for i in range(len(csv_paths)):
        df = pd.read_csv(csv_paths[i], sep='\t')
        sheet_name = Path(csv_paths[i]).stem
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()


if __name__ == '__main__':
    path = Path('data/excel1.xlsx')
    x = [1, 2, 3, 4, 5, 6, 7]
    y = [11, 12, 13, 14, 15, 16, 17]
    create_xmls(path)
    save_to_xmls(path, x, y, 'arkusz1')

