import sqlite3


# <QueryDict: {'csrfmiddlewaretoken': ['8pfYdedvqjfiOK4aDcJNGcYo8mJaZVWUK1hdQ38cDQIAC55VzDpdFGm7A6rR76YC'], 'arch': ['excel', ''],
# 'cabecera': [''], 'proveedores': ['Proveedor 1'], 'miles': ['sin_separador'], 'decimales': ['sin_separador'],
# 'cod_articulo': ['col1'], 'descripcion': ['col2'], 'precio': ['col3']}>

def insertar(datos):
    
    print(datos)

    datos_archivos = datos.getlist('arch')
    tipo_archivo = datos_archivos[0]
    delimitador = datos_archivos[1]
    cabecera = datos.get('cabecera')
    proveedor = datos.get('proveedores')
    separador_miles = datos.get('miles')
    separador_decimales = datos.get('decimales')
    codigo_articulo = datos.get('cod_articulo')
    descripcion_articulo = datos.get('descripcion')
    precio_articulo = datos.get('precio')


    ##INSERT EN CONFIGURACION LISTAS
    try:
        sqliteConnection = sqlite3.connect('huellitas.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        
        sqlite_insert_query = """INSERT INTO gestionStock_configuracion_listas
                          (cabecera, tipo_archivo, proveedor_id, delimitador) 
                            VALUES (?, ?, ?, ?);"""
        
        data_tuple = (cabecera, tipo_archivo, proveedor, delimitador)
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into gestionStock_configuracion_listas table")

        cursor.close()



    ##PIDO EL ID(PK) DEL INSERT ANTERIOR
    
        sqliteConnection = sqlite3.connect('huellitas.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        
        sqlite_select_query = """SELECT id FROM gestionStock_configuracion_listas
                          WHERE proveedor_id = ? """
        cursor.execute(sqlite_select_query, (proveedor,))
        id = cursor.fetchall()
        
        print(id[0][0])
        id = id[0][0]
        print("Python Variables inserted successfully into gestionStock_configuracion_listas table")

        cursor.close()

 
    ##INSERT EN CONFIGURACION COLUMNAS
    
    
        sqliteConnection = sqlite3.connect('huellitas.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        
        sqlite_insert_query = """INSERT INTO gestionStock_configuracion_columnas
                          (decimal, columna_archivo, columna_bd, miles, lista_id) 
                            VALUES (?, ?, ?, ?, ?);"""

        ##CODIGO ARTICULO
        data_tuple = ('', codigo_articulo,'codigo_articulo', '', int(id))
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()

        ##DESCRIPCION ARTICULO
        cursor = sqliteConnection.cursor()
        sqlite_insert_query = """INSERT INTO gestionStock_configuracion_columnas
                          (decimal, columna_archivo, columna_bd, miles, lista_id) 
                            VALUES (?, ?, ?, ?, ?);"""
        data_tuple = ('', descripcion_articulo,'descripcion_articulo', '', int(id))
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()

        ##PRECIO ARTICULO
        cursor = sqliteConnection.cursor()
        sqlite_insert_query = """INSERT INTO gestionStock_configuracion_columnas
                          (decimal, columna_archivo, columna_bd, miles, lista_id) 
                            VALUES (?, ?, ?, ?, ?);"""
        data_tuple = (separador_decimales, precio_articulo,'precio_articulo', separador_miles, int(id))
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()
        
        print("Python Variables inserted successfully into gestionStock_configuracion_columnas table")

      

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


