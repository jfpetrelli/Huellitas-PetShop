from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from gestionStock.models import Proveedores, Localidades
from gestionStock.forms import ProveedoresForm


class Home(TemplateView):
    template_name = "home.html"


class ProveedoresList(ListView):
    model = Proveedores
    queryset = model.objects.all()
    context_object_name = "proveedores"
    template_name = "proveedores.html"

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
    template_name = 'proveedores_confirm_delete.html'
    success_url = reverse_lazy('proveedor_list')




def almacenes(request):

    return render(request,"almacen.html")

def resumen(request):

    return render(request,"resumen.html")

def configuracion(request):

    return render(request,"configuracion.html")

def login(request):

    return render(request,"login.html")



    



