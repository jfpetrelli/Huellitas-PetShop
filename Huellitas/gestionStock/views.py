from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import FileResponse
from gestionStock.models import Proveedores, Localidades, Articulos, Configuracion_Listas, Configuracion_Columnas
from gestionStock.forms import ProveedoresForm, ArticulosForm, ConfiguracionListForm, OrdenCompra
from django.contrib.auth.views import LoginView, LogoutView
from gestionStock.controller import configuracion_archivos as ca, insertar as ins, insertar_lista as ins_list
import os, io
#OrdenCompra
from reportlab.pdfgen import canvas
from gestionStock.models import Tmp_Orden_Compra
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm
from django.views.generic import View


#LOGIN-LOGOUT
class Login(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class Logout(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        return super().dispatch(request, *args, **kwargs)

#HOME
class Home(TemplateView):
    template_name = "home.html"


#PROVEEDORES
class ProveedoresList(ListView):
    model = Proveedores
    queryset = model.objects.all()
    context_object_name = "proveedores"
    template_name = "proveedores.html"
    paginate_by = 20

    def get_queryset(self): # new
        query = self.request.GET.get('buscar')
        if query:
            object_list = Proveedores.objects.filter(
                Q(razon_social__icontains=query) | Q(cuit__icontains=query)
            )
        else:
            object_list = Proveedores.objects.all()
        return object_list

class ProveedoresUpdate(UpdateView):
    model = Proveedores
    template_name = "proveedor.html"
    form_class = ProveedoresForm
    success_url = reverse_lazy('proveedor_list')

class ProveedoresCreate(CreateView):
    model = Proveedores
    form_class = ProveedoresForm
    template_name = "proveedor.html"
    success_url = reverse_lazy('proveedor_list')

class ProveedoresDelete(DeleteView):
    model = Proveedores
    template_name = "proveedores_confirm_delete.html"
    success_url = reverse_lazy('proveedor_list')


##ALMACENES
class ArticulosList(ListView):
    model = Articulos
    queryset = model.objects.all()
    context_object_name = "articulos"
    template_name = "almacen.html"
    paginate_by = 20

    def get_queryset(self): # new
        query = self.request.GET.get('buscar')
        print(query)
        if query:
            object_list = Articulos.objects.filter(
                Q(descripcion__icontains  = query) | Q(proveedor__razon_social__icontains=query))
        else:
            object_list = Articulos.objects.all()
        return object_list

class ArticuloUpdate(UpdateView):
    model = Articulos
    template_name = "articulo.html"
    form_class = ArticulosForm
    success_url = reverse_lazy('articulo_list')

class ArticuloCreate(CreateView):
    model = Articulos
    form_class = ArticulosForm
    template_name = "articulo.html"
    success_url = reverse_lazy('articulo_list')

class ArticuloDelete(DeleteView):
    model = Articulos
    template_name = "articulo_confirm_delete.html"
    success_url = reverse_lazy('articulo_list')


##CONFIGURACION DE LISTAS
def art_prov(request):

    return render(request,"art_prov.html")

def configuracion(request):

    proveedores = Proveedores.objects.all()


    if "GET" == request.method:
        return render(request,"configuracion.html",{'proveedores': proveedores})
    else:
        data = list()
        split_tup = os.path.splitext(request.FILES["file"].name)

        if request.POST.get('tipo_archivo') == 'excel' and (split_tup[1] == '.xlsx' or split_tup[1] == '.xls'):
            arch = request.FILES["file"]
            data = ca.excel(arch)

        if request.POST.get('tipo_archivo') == 'csv' and split_tup[1] == '.csv':
            arch = request.FILES["file"]
            delim = request.POST.get('delimitador')
            print(delim)
            if delim == '': 
                return render(request,"error_tipo_archivo_extension.html")
            else:
                data = ca.txt_del(arch, delim)

        if request.POST.get('tipo_archivo') == 'txt' and split_tup[1] == '.txt':
            arch = request.FILES["file"]
            delim = request.POST.get('delimitador')
            if delim == '': 
                return render(request,"error_tipo_archivo_extension.html")
            else:
                data = ca.txt_del(arch,delim)

        if len(data) == 0:
            data = None
            return render(request,"error_tipo_archivo_extension.html")
        
        num_colums = list()
        for i in range(0,len(data[0])):
            num_colums.append(i+1)
        
        arch_delim = list()
        arch_delim.append(request.POST.get('tipo_archivo'))
        arch_delim.append(request.POST.get('delimitador'))
        print(proveedores)
        return render(request,"configuracion.html", {'data': data, 'proveedores': proveedores, 'num_colums': num_colums, 'arch_delim': arch_delim})

def vincular_configuracion(request):
    
    if request.method == "POST":
        
        configuracion_listas = Configuracion_Listas.objects.filter(proveedor_id=request.POST.get('proveedores')).exists()
        if configuracion_listas:
            return render(request, "no_vinculado.html")

        ins.insertar(request.POST)
      
    return render(request, "vinculado_configuracion.html")

class ConfigurarList(ListView):
    model = Configuracion_Listas
    queryset = model.objects.all()
    context_object_name = "configuracion_list"
    template_name = "configuracion_list.html"
    paginate_by = 20

    def get_queryset(self): # new
        query = self.request.GET.get('buscar')
        if query:
            object_list = Configuracion_Listas.objects.filter(
                Q(proveedor__icontains=query)
            )
        else:
            object_list = Configuracion_Listas.objects.all()
        return object_list

class ConfigurarListDelete(DeleteView):
    model = Configuracion_Listas
    template_name = "configurar_list_confirm_delete.html"
    success_url = reverse_lazy('configuracion_list')

def importar_lista(request):
    proveedores = Proveedores.objects.all()
    if "GET" == request.method:
        return render(request,"importar_lista.html",{'proveedores': proveedores})
    
    proveedor = request.POST.get('proveedores')


    split_tup = os.path.splitext(request.FILES["file"].name)
    tipo_archivo = ''
    tipo_extension = split_tup[1]
    tipo_archivo_list = list(Configuracion_Listas.objects.filter(proveedor=proveedor).values_list('tipo_archivo'))
    if tipo_archivo_list == []:
        return render(request,"error_importar_lista_proveedor.html")
    print(tipo_archivo_list[0][0])
    if tipo_archivo_list[0][0] == 'excel':
        tipo_archivo = '.xls'
    if  tipo_archivo_list[0][0] == 'csv':
        tipo_archivo = '.csv'
    if  tipo_archivo_list[0][0] == 'txt':
        tipo_archivo = '.txt'
    if tipo_extension == '.xlsx':
        tipo_extension = '.xls'
    
    print(tipo_archivo, tipo_extension)
    
    if tipo_extension == tipo_archivo:
        ins_list.insertar_lista(proveedor, request.FILES["file"])
        return render(request,"importar_lista.html", {'proveedores': proveedores})

    return render(request,"error_importar_lista.html")

def resumen(request):

    return render(request,"resumen.html")

class ordenCompraList(ListView):
    model = Tmp_Orden_Compra
    queryset = model.objects.all()
    context_object_name = "ordenCompra"
    template_name = "ordenCompra.html"
    paginate_by = 20

    def get_queryset(self): # new
        query = self.request.GET.get('buscar')
        if query:
            object_list = Tmp_Orden_Compra.objects.filter(
                Q(proveedor__razon_social__icontains=query))
        else:
            object_list = Tmp_Orden_Compra.objects.all()
        return object_list


class ordenCompraPDF(View):
    def cabecera(self, pdf):
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(200, 790, u"ORDEN DE COMPRA")
        pdf.drawString(200, 770, u"Proveedor")

    def tabla(self, pdf, y):
        # Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Codigo', 'Descripcion', 'Precio', 'Cantidad')
        # Creamos una lista de tuplas que van a contener a las personas
        renglones = Tmp_Orden_Compra.objects.all()
        detalles = []
        for renglon in renglones:
            detalles.append((renglon.articulo_proveedor, renglon.descripcion,
                             renglon.precio_costo, renglon.cantidad))
        # Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[5 * cm, 5 * cm, 5 * cm, 5 * cm])
        # Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                # La primera fila(encabezados) va a estar centrada
                ('ALIGN', (0, 0), (3, 0), 'CENTER'),
                # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        # Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        # Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60, y)

    def get(self, request, *args, **kwargs):
        # Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        # Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf, y)
        # Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response