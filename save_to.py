import pandas as pd
from pathlib import Path


def save_to_csv(path, parameters, x, y):
    str1 = parameters.get('wartości x')
    str2 = parameters.get('wartości y')
    parameters.pop('wartości x')
    parameters.pop('wartości y')
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
