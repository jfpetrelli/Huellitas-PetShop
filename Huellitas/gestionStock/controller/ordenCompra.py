import sqlite3

def persistir_OC (detalle, proveedor):
    id = insertar_OrdenCompra(detalle, proveedor)
    return id

def insertar_OrdenCompra(detalle,proveedor):

    try:
        sqliteConnection = sqlite3.connect('huellitas.sqlite3')
        cursor = sqliteConnection.cursor()
        sqlite_insert_query = """INSERT INTO gestionStock_ordencompra
                          (descripcion, proveedor_id) 
                            VALUES (?, ?);"""

        data_tuple = ('detalle', 2)
        print("2")
        cursor.execute(sqlite_insert_query, data_tuple)
        print("3")
        sqliteConnection.commit()
        print("4")
        id = cursor.lastrowid
        print(id)
        cursor.close()
        return id
    except sqlite3.Error as error:
        print('error al crear OC')
        return 'XXX'
    finally:
        if sqliteConnection:
            sqliteConnection.close()

