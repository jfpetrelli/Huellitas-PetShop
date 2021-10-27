
import pandas as pd


def excel(excel_file):
    df = pd.read_excel(io = excel_file, sheet_name="Sheet1") 
    lista = df.values.tolist()
    lista.insert(0,df.columns.values.tolist())
    print(lista)
    return lista

def txt_del(txt_file, delimitador):
    if delimitador == 'coma':
        delimitador = ','
    if delimitador == 'p-coma':
        delimitador = ';'
    if delimitador == 'tab':
        delimitador = '\t'
    df = pd.read_table(txt_file, sep = delimitador)
    lista = df.values.tolist()
    lista.insert(0,df.columns.values.tolist())
    print(lista) 
    return lista