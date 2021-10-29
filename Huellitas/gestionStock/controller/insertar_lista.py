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
    conf_columnas = Configuracion_Columnas.objects.filter(lista=conf_lista_list[0][0]).values_list('decimal','columna_archivo','columna_bd')
    conf_columnas_list = list(conf_columnas)
    print(conf_lista_list)
    print(conf_columnas_list)

    #DATOS SOBRE LA LISTA
    proveedor = proveedor
    cabecera = 0
    if conf_lista_list[0][2] == '':
        cabecera = 0
    else:
        cabecera = int(conf_lista_list[0][2])
    tipo_archivo = conf_lista_list[0][3]
    delimitador = conf_lista_list[0][4]
    
    #DATOS SOBRE LAS COLUMNAS
    codigo_articulo_str = conf_columnas_list[0][1]
    codigo_articulo = int(codigo_articulo_str[3])
    descripcion_articulo_str = conf_columnas_list[1][1]
    descripcion_articulo = int(descripcion_articulo_str[3])
    precio_articulo_str = conf_columnas_list[2][1]
    precio_articulo = int(precio_articulo_str[3])
    separador_decimal = conf_columnas_list[2][0]



    print(lista_proveedor)
    lista_datos = list()
    if tipo_archivo == 'excel':
        df = pd.read_excel(io = lista_proveedor) 
        lista_datos = df.values.tolist()
        lista_datos.insert(0,df.columns.values.tolist())
        print(lista_datos)
    else:
        if delimitador == 'coma':
            delimitador = ','
        if delimitador == 'p-coma':
            delimitador = ';'
        if delimitador == 'tab':
            delimitador = '\t'
        df = pd.read_table(lista_proveedor, sep = delimitador)
        lista_datos = df.values.tolist()
        lista_datos.insert(0,df.columns.values.tolist())
        print(lista_datos) 

    lista_datos_acotada = lista_datos[cabecera:]
    print(lista_datos_acotada)

    delete_tabla_tmp()

    for arreglo in lista_datos_acotada:

        precio_nuevo = convertir_precio(arreglo[precio_articulo-1], separador_decimal)

        if precio_nuevo == -1:
            continue
        
        #EXISTE EL ARTICULO EN LA BD?
        #SI NO EXISTE INSERTA
        # SI EXISTE ACTUALIZA
        if list(Articulos.objects.filter(proveedor=proveedor, articulo_proveedor = arreglo[codigo_articulo-1])) == []:
            insertar_articulo(proveedor, arreglo[codigo_articulo-1],arreglo[descripcion_articulo-1],precio_nuevo)
            insertar_tabla_tmp(True, proveedor, arreglo[codigo_articulo-1],arreglo[descripcion_articulo-1],precio_nuevo)
        else:
            actualizar_articulo(proveedor, arreglo[codigo_articulo-1],arreglo[descripcion_articulo-1], precio_nuevo)
            insertar_tabla_tmp(False, proveedor, arreglo[codigo_articulo-1],arreglo[descripcion_articulo-1],precio_nuevo)


def delete_tabla_tmp():

    try:
        sqliteConnection = sqlite3.connect('huellitas.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_query = """DELETE from gestionStock_tmp_articulos"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        sql_update_query = """UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='gestionStock_tmp_articulos';"""
        cursor.execute(sql_update_query)
        sqliteConnection.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def insertar_tabla_tmp(nuevo, proveedor, art_prov,descripcion,precio_nuevo):
       
    
    try:
        sqliteConnection = sqlite3.connect('huellitas.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        
        sqlite_insert_query = """INSERT INTO gestionStock_tmp_articulos
                          (nuevo, proveedor_id, descripcion, articulo_proveedor, precio_costo) 
                            VALUES (?, ?, ?, ?, ?);"""
        

        data_tuple = (nuevo, proveedor, descripcion, art_prov, precio_nuevo)
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into gestionStock_articulos table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


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
        print("Python Variables inserted successfully into gestionStock_articulos table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



def actualizar_articulo(proveedor, codigo_articulo, descripcion_articulo, precio_articulo):
    
    print('Proveedor ' + proveedor)
       ##INSERT ARTICULO
    try:
        sqliteConnection = sqlite3.connect('huellitas.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        
        sqlite_insert_query = """UPDATE gestionStock_articulos set
                            precio_costo = ?, fecha_actualizacion = ?
                            WHERE articulo_proveedor = ? AND proveedor_id = ?;"""
        
        data_tuple = (precio_articulo, date.today(), codigo_articulo, proveedor)
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        print("Python Variables update successfully into gestionStock_articulos table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def convertir_precio(precio, separador_decimal):
    
    if precio == '':
        return 0
    
    if type(precio) != float and type(precio) != int:
        if not any(chr.isdigit() for chr in precio):
            return -1

    if separador_decimal == 'punto':
        separador_decimal = '.'
    if separador_decimal == 'coma':
        separador_decimal = ','
    

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
