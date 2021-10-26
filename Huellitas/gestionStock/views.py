from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from gestionStock.models import Proveedores, Localidades, Articulos, Configuracion_Listas, Configuracion_Columnas
from gestionStock.forms import ProveedoresForm, ArticulosForm, ConfiguracionListForm
from django.contrib.auth.views import LoginView, LogoutView
from gestionStock.logica import configuracion_archivos as ca, insertar as ins

import os
import sqlite3

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
    paginate_by = 5

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
    paginate_by = 5

    def get_queryset(self): # new
        query = self.request.GET.get('buscar')
        if query:
            object_list = Articulos.objects.filter(
                Q(descripcion__icontains  = query))
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
        print(split_tup[1])

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

        if request.POST.get('tipo_archivo') == 'txt_del' and split_tup[1] == '.txt':
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
    paginate_by = 5

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


##LOGIN
def login(request):

    return render(request,"login.html")



    

def resumen(request):

    return render(request,"resumen.html")

