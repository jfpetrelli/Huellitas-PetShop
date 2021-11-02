from django.core.mail import EmailMessage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import datetime
import io
import sqlite3

from reportlab.platypus import Table, TableStyle


def mail(proveedor):
    pdf = generar_pdf(proveedor)
    fecha_actual = datetime.datetime.now().strftime("%A, %d de %B %Y %I:%M %p")
    msj = "Se cargo un un nuevo archivo de articulos"
    email = EmailMessage('Lista actualizada', msj,'seminarioe2etest@gmail.com', ['seminarioe2etest@gmail.com'])
    email.attach(f'ListaCargada-{fecha_actual}.pdf', pdf)
    email.send()
    print('email enviado')

def generar_pdf(proveedor):
    nuevos, actualizados = articulos_temporales()
    def cabecera(pdf):
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 20)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(120, 800, u"Informe de nueva lista de articulos cargada")
        pdf.setFont("Helvetica", 13)
        pdf.drawString(20, 770, u"Proveedor: " + proveedor)
        # Obtengo fecha
        ahora = datetime.datetime.now()
        fecha_actual = ahora.strftime("%A, %d de %B %Y %I:%M %p")
        pdf.drawString(20, 750, u"Fecha: " + fecha_actual)

    def cuerpo(pdf, nuevos, actualizados):
        pdf.setFont("Helvetica", 13)
        pdf.drawString(20, 730, u"Articulos nuevos: " + str(len(nuevos)))
        pdf.drawString(20, 710, u"Articulos actualizados: " + str(len(actualizados)))

    def tabla(pdf, nuevos, actualizados):

        # Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Codigo', 'Descripcion', 'Precio','Estado')
        # Creamos una lista de tuplas que van a contener informacion
        detalles = []


        for renglon in nuevos:
            print(renglon)
            if int(renglon[1]) == 1:
                est = 'Nuevo'
            else:
                est = 'Actualizado'
            detalles.append((str(renglon[2]), str(renglon[3]),
                             str(renglon[4]), est))
        for renglon in actualizados:
            print(renglon)
            if int(renglon[1]) == 1:
                est = 'Nuevo'
            else:
                est = 'Actualizado'
            detalles.append((str(renglon[3]), (str(renglon[4])[:30]),
                             str(renglon[5]), est))

        # Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[3 * cm, 8 * cm, 2 * cm, 2 * cm])
        # Establecemos el tamaño de la hoja que ocupará la tabla

        cant = len(detalles)
        detalle_orden.wrapOn(pdf, 0, 400)
        detalle_orden.drawOn(pdf, 50, 640 - (18*cant))



     # array de bytes, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
       # Canvas nos permite hacer el reporte con coordenadas X y Y
    fecha_actual = datetime.datetime.now().strftime("%d/%B/%Y")
    titulo = f'Lista-{proveedor}-{fecha_actual}'
    pdf = canvas.Canvas(buffer, pagesize=A4)
    # Titulo
    pdf.setTitle(titulo)
    # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    cabecera(pdf)
    cuerpo(pdf, nuevos, actualizados)
    tabla(pdf, nuevos, actualizados)
#       y = 600
#       self.tabla(pdf, y)
        # Con show page hacemos un corte de página para pasar a la siguiente
    pdf.showPage()
    pdf.save()
    p = buffer.getvalue()
    return p

def articulos_temporales():
    try:
        sqliteConnection = sqlite3.connect('huellitas.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_query_nuevos = """SELECT * FROM gestionStock_tmp_articulos
                                WHERE nuevo = TRUE;"""
        sqlite_query_actualizados = """SELECT * FROM gestionStock_tmp_articulos
                                        WHERE nuevo = FALSE;"""
        cursor.execute(sqlite_query_nuevos)
        nuevos = cursor.fetchall()
        cursor.execute(sqlite_query_actualizados)
        actualizados = cursor.fetchall()
        sqliteConnection.commit()

        cursor.close()
        print( nuevos)
        return nuevos, actualizados

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
