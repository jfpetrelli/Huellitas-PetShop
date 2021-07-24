
import pandas as pd


def excel(excel_file):
    df = pd.read_excel(io = excel_file, sheet_name="Sheet1")  
    return df.values.tolist()

def txt_del(txt_file, delimitador):
    if delimitador == 'coma':
        delimitador = ','
    if delimitador == 'p-coma':
        delimitador = ';'
    if delimitador == 'tab':
        delimitador = '\t'
    df = pd.read_table(txt_file, sep = delimitador)
    print(df) 
    return df.values.tolist()