import sqlite3
from gestionStock.models import Configuracion_Listas, Configuracion_Columnas, Articulos
import pandas as pd
from django.core import serializers
from datetime import date

#[(15, 1, '1', 'excel', '')]
#[('', '', 'col1', 'codigo_articulo'), ('', '', 'col2', 'descripcion_articulo'), 
# ('sin_separador', 'sin_separador', 'col3', 'precio_articulo')]

def insertar_lista(proveedor, lista_proveedor):
    #BUSCAR DATOS EN BD
    conf_lista = Configuracion_Listas.objects.filter(proveedor=proveedor).values_list('pk','proveedor','cabecera','tipo_archivo','delimitador')
    #data = serializers.serialize("json", Configuracion_Listas.objects.filter(proveedor=proveedor), fields=('proveedor','cabecera','tipo_archivo','delimitador'))
    conf_lista_list = list(conf_lista)
    conf_columnas = Configuracion_Columnas.objects.filter(lista=conf_lista_list[0][0]).values_list('decimal','miles','columna_archivo','columna_bd')
    conf_columnas_list = list(conf_columnas)
    print(conf_lista_list)
    print(conf_columnas_list)

    #DATOS SOBRE LA LISTA
    proveedor = proveedor
    cabecera = int(conf_lista_list[0][2])
    tipo_archivo = conf_lista_list[0][3]
    delimitador = conf_lista_list[0][4]
    
    #DATOS SOBRE LAS COLUMNAS
    codigo_articulo_str = conf_columnas_list[0][2]
    codigo_articulo = int(codigo_articulo_str[3])
    descripcion_articulo_str = conf_columnas_list[1][2]
    descripcion_articulo = int(descripcion_articulo_str[3])
    precio_articulo_str = conf_columnas_list[2][2]
    precio_articulo = int(precio_articulo_str[3])
    separador_decimal = conf_columnas_list[2][0]
    separador_mil = conf_columnas_list[2][1]


    print(lista_proveedor)
    lista_datos = list()
    if tipo_archivo == 'excel':
        df = pd.read_excel(io = lista_proveedor, sheet_name="Sheet1") 
        lista_datos = df.values.tolist()
        lista_datos.insert(0,df.columns.values.tolist())
        print(lista_datos)
    
    lista_datos_acotada = lista_datos[cabecera:]
    print(lista_datos_acotada)
    for arreglo in lista_datos_acotada:

        precio_nuevo = convertir_precio(arreglo[precio_articulo-1], separador_decimal, separador_mil)

        #EXISTE EL ARTICULO EN LA BD?
        #SI NO EXISTE INSERTA
        # SI EXISTE ACTUALIZA
        if list(Articulos.objects.filter(proveedor=proveedor, articulo_proveedor = arreglo[codigo_articulo-1])) == []:
            insertar_articulo(proveedor, arreglo[codigo_articulo-1],arreglo[descripcion_articulo-1],precio_nuevo)
        else:
            actualizar_articulo(proveedor, arreglo[codigo_articulo-1],arreglo[descripcion_articulo-1], precio_nuevo)




def insertar_articulo(proveedor, codigo_articulo, descripcion_articulo, precio_articulo):
       
    print('Proveedor ' + proveedor)
       ##INSERT ARTICULO
    try:
        sqliteConnection = sqlite3.connect('huellitas.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        
        sqlite_insert_query = """INSERT INTO gestionStock_articulos
                          (proveedor_id, articulo_proveedor, descripcion, precio_costo, stock, precio_vta, fecha_actualizacion, marca, tipo) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        
        

        data_tuple = (proveedor, codigo_articulo, descripcion_articulo, precio_articulo, 0, 0, date.today(),'','')
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into gestionStock_configuracion_listas table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



def actualizar_articulo(proveedor, codigo_articulo, descripcion_articulo, precio_articulo):
    pass

def convertir_precio(precio, separador_decimal, separador_mil):
    
    if precio == '':
        return 0

    if type(precio) == int:
       return float(precio)
    if type(precio) == float:
        return float(precio)
    
    sep = precio.find(separador_decimal)
    if sep == -1:
        return float(''.join(filter(str.isnumeric,precio)))
    
    corte1 = precio[:sep]
    corte2 = precio[sep+1:]
    
    precio_mil = ''.join(filter(str.isnumeric,corte1))
    precio_decimal = ''.join(filter(str.isnumeric,corte2))
    return float(precio_mil + '.' + precio_decimal)
