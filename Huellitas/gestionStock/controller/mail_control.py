from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
import datetime
import io


def mail(proveedor):
    pdf = generar_pdf(proveedor)
    email = EmailMessage('Lista actualizada', 'el mensaje','seminarioe2etest@gmail.com', ['seminarioe2etest@gmail.com'])
    email.attach('ejemplo1.pdf', pdf)
    email.send()
    print('enviado')

def generar_pdf(proveedor):

    def cabecera(pdf):
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 20)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(120, 800, u"Lista de articulos HUELLITAS")
        pdf.setFont("Helvetica", 13)
        pdf.drawString(20, 710, u"Proveedor: " + proveedor)
        # Obtengo fecha
        ahora = datetime.datetime.now()
        fecha_actual = ahora.strftime("%A, %d de %B %Y %I:%M %p")
        pdf.drawString(20, 690, u"Fecha: " + fecha_actual)

    # def tabla(self, pdf, y):
    #     # Creamos una tupla de encabezados para neustra tabla
    #     encabezados = ('Codigo', 'Descripcion', 'Precio', 'Cantidad')
    #     # Creamos una lista de tuplas que van a contener a las personas
    #     query = self.request.GET.get('buscar')
    #     renglones = object_list = Tmp_Orden_Compra.objects.filter(
    #         Q(proveedor__razon_social__icontains=query))
    #     detalles = []
    #     cantidad = 0
    #     total = 0
    #     for renglon in renglones:
    #         detalles.append((renglon.articulo_proveedor, renglon.descripcion,
    #                          renglon.precio_costo, renglon.cantidad))
    #         cantidad = cantidad + renglon.cantidad
    #         total = total + (renglon.cantidad * renglon.precio_costo)
    #     txt = f"Total de articulos = {cantidad}  total = ${total}"
    #     pdf.drawString(20, 670, txt)
    #     # Establecemos el tamaño de cada una de las columnas de la tabla
    #     detalle_orden = Table([encabezados] + detalles, colWidths=[5 * cm, 3 * cm, 2 * cm])
    #     # Aplicamos estilos a las celdas de la tabla
    #     detalle_orden.setStyle(TableStyle(
    #         [
    #             # La primera fila(encabezados) va a estar centrada
    #             ('ALIGN', (0, 0), (3, 0), 'CENTER'),
    #             # Los bordes de todas las celdas serán de color negro y con un grosor de 1
    #             ('GRID', (0, 0), (-1, -1), 1, colors.black),
    #             # El tamaño de las letras de cada una de las celdas será de 10
    #             ('FONTSIZE', (0, 0), (-1, -1), 10),
    #         ]
    #     ))
    #     # Establecemos el tamaño de la hoja que ocupará la tabla
    #     detalle_orden.wrapOn(pdf, 800, 600)
    #     # Definimos la coordenada donde se dibujará la tabla
    #     detalle_orden.drawOn(pdf, 60, y)


     # array de bytes, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
       # Canvas nos permite hacer el reporte con coordenadas X y Y
    fecha_actual = datetime.datetime.now().strftime("%d/%B/%Y")
    titulo = f'Lista-{proveedor}-{fecha_actual}'
    pdf = canvas.Canvas(buffer)
    # Titulo
    pdf.setTitle(titulo)
    # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    cabecera(pdf)
#       y = 600
#       self.tabla(pdf, y)
        # Con show page hacemos un corte de página para pasar a la siguiente
    pdf.showPage()
    pdf.save()
    p = buffer.getvalue()
    return p
